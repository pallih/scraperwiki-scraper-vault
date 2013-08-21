# Minneapolis provides aggregate crime data by neighborhood
# http://www.minneapolismn.gov/police/statistics/crime-statistics_codefor_statistics

# Some code borrowed from:
# https://scraperwiki.com/scrapers/corresponding_local_authorities/edit/

import scraperwiki
import requests
import openpyxl
import xlrd
import tempfile
import time
import pprint
import re

stats = ['total', 'homicide', 'rape', 'robbery', 'agg_assault', 'burglary', 'larceny', 'auto_theft', 'arson']

default_fields = {
    'neighborhood': 0,
    'total': 1,
    'homicide': 2,
    'rape': 3,
    'robbery': 4,
    'agg_assault': 5,
    'burglary': 6,
    'larceny': 7,
    'auto_theft': 8,
    'arson': 9
}

blank_row = {
    'year': 2013,
    'month': 1,
    'notes': '',
    'neighborhood': '',
    'neighborhood_key': '',
    'total': 0,
    'homicide': 0,
    'rape': 0,
    'robbery': 0,
    'agg_assault': 0,
    'burglary': 0,
    'larceny': 0,
    'auto_theft': 0,
    'arson': 0
}

neighborhood_list = {}

n_translate_keys = {
    'camden_ind_area': 'camden_industrial',
    'columbia': 'columbia_park',
    'phillips_east': 'east_phillips',
    'fowell': 'folwell',
    'humboldt_ind_area': 'humboldt_industrial_area',
    'phillips_midtown': 'midtown_phillips',
    'nicollet_island': 'nicollet_island_east_bank',
    'north_river_ind_area': 'north_river_industrial_area',
    'northrup': 'northrop',
    'prospect_park': 'prospect_park_east_river',
    'prospect_park_east_river_rd': 'prospect_park_east_river',
    'prospect_park_east_river_road': 'prospect_park_east_river',
    'steven_s_square_loring_heights': 'stevens_square_loring_heights',
    'stevens_square': 'stevens_square_loring_heights',
    'stevens_square_loring_hgts': 'stevens_square_loring_heights',
    'u_of_m': 'university_of_minnesota',
}

# north_river_industrial_area was annexed by mckinley in 1996 (reports included through 2006) 
# http://www.ci.minneapolis.mn.us/neighborhoods/mckinley/index.htm
#
# Bad data in 2013-03 spreadsheet
n_combinations = {
    'north_river_industrial_area': 'mckinley',
    'minneahaha': 'minnehaha',
}


# Parse a string into an integer first, then float
def parse_num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except ValueError:
            return 0


# Get an integer value from the variables table
def get_int_var(name, default, max):
    var = scraperwiki.sqlite.get_var(name, default)
    if var >= max:
        var = default
        
    return var


# Turn string into a key
def string_to_key(str):
    str = re.sub('[^0-9a-zA-Z]+', '_', str)
    str = str.replace('__', '_')
    str = str.replace('__', '_')
    return str.lower()


# Turn neighborhood name into a key, with translation
# for consistency
def get_neighborhood_key(str):
    key = string_to_key(str)
    if key in n_translate_keys:
        key = n_translate_keys[key]
        
    return key


# Get the definitive list of neighborhoods
def get_neighborhoods():
    scraperwiki.sqlite.attach('minneapolis_neighborhoods', asname = 'neighborhoods')
    n_query = scraperwiki.sqlite.select('* FROM `neighborhoods`.swdata ORDER BY neighborhood_key')
    for n in n_query:
        neighborhood_list[n['neighborhood_key']] = n


# Use the neighborhood list to get the definitive name
def get_neighborhood_name(key, name):
    if key in neighborhood_list:
        return neighborhood_list[key]['neighborhood']
    else:
        return name


# OpenPyXL version of open workbook
def get_workbook_openpyxl(url):
    # Loads an xlsx file from the internet
    raw = requests.get(url, verify=False).content
    f = tempfile.NamedTemporaryFile('wb')
    f.write(raw)
    f.seek(0)
    wb = openpyxl.load_workbook(f.name)
    f.close()
    return wb


# XLRD version of open workbook
def get_workbook_xlrd(url):
    xlbin = scraperwiki.scrape(url)
    wb = xlrd.open_workbook(file_contents = xlbin)
    return wb


# But data in start format, OpenPyXL version
def get_data_openpyxl(wb, sheet = 'Sheet1'):
    # Turn a sheet on a workbook into an array
    data = wb.get_sheet_by_name(sheet)
    return [[unicode(cell.value).strip() for cell in row] for row in data.rows]


# But data in start format, XLRD version
def get_data_xlrd(wb, sheet = 0):
    # Turn a sheet on a workbook into an array
    sheet = wb.sheet_by_index(sheet)
    data = []
    
    for rownum in range(0, sheet.nrows):
        values = [ unicode(c.value).strip() for c in sheet.row(rownum) ]
        data.append(values)
    
    return data


# Handles blank neighborhoods
def handle_missing_neighborhoods(year, month):
    select_query = "neighborhood_key FROM `swdata` WHERE neighborhood_key = '%s' AND year = %s AND month = %s"
    notes = 'Missing data, assuming no incidents.'
    
    for n in neighborhood_list:
        found = scraperwiki.sqlite.select(select_query % (n, year, month))
        if len(found) == 0:
            print 'Blank row needed for %s, %s-%s' % (n, year, month)
            new_row = blank_row
            new_row['year'] = year
            new_row['month'] = month
            new_row['notes'] = notes
            new_row['neighborhood'] = neighborhood_list[n]['neighborhood']
            new_row['neighborhood_key'] = n
            scraperwiki.sqlite.save(['neighborhood_key', 'year', 'month'], new_row)


# Handles combining of neighborhoods (not very elequently)
def handle_combinations(year, month):
    common_where = "neighborhood_key='%s' AND year = %s AND month = %s"
    find_query = "* FROM `swdata` WHERE " + common_where
    update_note_query = "UPDATE `swdata` SET notes = 'Added to %s' WHERE " + common_where

    for i, n in enumerate(n_combinations):
        # n is neighborhood to add from
        # c is neighborhood that is combining to
        c = n_combinations[n]

        # Check if this specific combination is needed
        n_check = scraperwiki.sqlite.select(find_query % (n, year, month))
        if len(n_check) == 0:
            continue

        # Get data from neighborhood n
        n_n = n_check[0]

        # Get data from neighborhood c
        n_c = scraperwiki.sqlite.select(find_query % (c, year, month))[0]

        # Make note in neighborhood n
        scraperwiki.sqlite.execute(update_note_query % (c, n, year, month))

        # Add data from neighborhood n to neighborhood c
        for i in stats:
            n_c[i] = n_c[i] + n_n[i]

        # Update and note neighborhood c
        update_combination = "UPDATE `swdata` SET notes = 'Added data from %s'"
        for i in stats:
            update_combination = update_combination + (", %s = %s" % (i, n_c[i]))

        update_combination = update_combination + " WHERE " + common_where
        scraperwiki.sqlite.execute(update_combination % (n, c, year, month))



# Make data given what year, month and fields there are
def make_data_row(r, year, month, fields):
    data = {
        'month': month,
        'year': year,
        'notes': ''
    }

    for f in fields:
        if fields[f] < len(r):
            if f == 'neighborhood':
                data['neighborhood_key'] = get_neighborhood_key(r[fields[f]])
                data[f] = get_neighborhood_name(data['neighborhood_key'], r[fields[f]])
            else:
                data[f] = parse_num(r[fields[f]])

    return data


# Process a workbook
def process_wb(url, year, month, file_type = 'xlsx', sheet = 0, start_row = 1, skip_rows = [], fields = default_fields):

    # Determine what format it is process accordingly
    if file_type == 'xlsx':
        wb = get_workbook_openpyxl(url)
        rows = get_data_openpyxl(wb, wb.get_sheet_names()[0])
    else:
        wb = get_workbook_xlrd(url)
        rows = get_data_xlrd(wb, sheet)

    # Go through rows and save.  For combining data, we look to see
    # if the combination keys are in this worksheet, then combine after
    # data has been entered
    combination_needed = False
    for i, r in enumerate(rows):
        if i >= start_row and i not in skip_rows:
            data = make_data_row(r, year, month, fields)
            scraperwiki.sqlite.save(['neighborhood_key', 'year', 'month'], data)

            # Check if combination is needed
            if data['neighborhood_key'] in n_combinations:
                combination_needed = True

    # If combination is needed, process.
    if combination_needed:
        print 'Combination needed for: %s-%s' % (year, month)
        handle_combinations(year, month)

    # There are many occasions where data is not available
    # for specific neighborhoods.  It is unknown if this is
    # a lack of data or that there were no crimes in this
    # neighborhood.  Let's assume it means there
    # was no crime in these neighborhoods
    handle_missing_neighborhoods(year, month)



# Process reports, save place
def process_reports(reports):
    get_neighborhoods()

    # Reset report placeholder
    #scraperwiki.sqlite.save_var('last_report', 0)

    try:
        last_report = get_int_var('last_report', 0, len(reports) - 1)
        print "All reports: %s" % len(reports)
        print "Last report: %s" % last_report
        
        for i, r in enumerate(reports):
            if i >= last_report:
                process_wb(**r)
                scraperwiki.sqlite.save_var('last_report', i)
            
    except scraperwiki.CPUTimeExceededError:
        # This just makes sure the scraper is not marked
        # as erroring even if it times out
        pass


reports = [

    # 2013 at the bottom of the list, so that the scraper can more easily continue where it left off.
    
    # 2012
    {
        'year': 2012,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097343.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097344.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-104694.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097346.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097347.xlsx',
    },
    {
        'year': 2012,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097348.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-097349.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-098066.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-100167.xls',
        'file_type': 'xls'
    },
    {
        'year': 2012,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-100563.xlsx',
    },
    {
        'year': 2012,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-101727.xlsx',
    },
    {
        'year': 2012,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-102903.xlsx',
    },
    
    # 2011
    {
        'year': 2011,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-084373.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-083122.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-090851.xlsx'
    },
    {
        'year': 2011,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067113.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067111.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067109.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067107.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067123.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067121.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067119.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067117.xls',
        'file_type': 'xls'
    },
    {
        'year': 2011,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067115.xls',
        'file_type': 'xls'
    },
    
    # 2010
    {
        'year': 2010,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067143.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067141.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067139.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067137.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067135.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067133.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067130.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067128.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067127.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067149.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067147.xls',
        'file_type': 'xls'
    },
    {
        'year': 2010,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067145.xls',
        'file_type': 'xls'
    },
    
    # 2009
    {
        'year': 2009,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067337.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067336.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067335.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067334.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067333.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067344.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067343.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067342.xls',
        'file_type': 'xls',
        'fields': {
            'neighborhood': 0,
            'total': 1,
            'rape': 2,
            'robbery': 3,
            'agg_assault': 4,
            'burglary': 5,
            'larceny': 6,
            'auto_theft': 7,
            'arson': 8
        }
    },
    {
        'year': 2009,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067341.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067340.xls',
        'file_type': 'xls'
    },
    {
        'year': 2009,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067339.xls',
        'file_type': 'xls',
        'fields': {
            'neighborhood': 0,
            'total': 1,
            'rape': 2,
            'robbery': 3,
            'agg_assault': 4,
            'burglary': 5,
            'larceny': 6,
            'auto_theft': 7,
            'arson': 8
        }
    },
    {
        'year': 2009,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-067338.xls',
        'file_type': 'xls'
    },
    
    # 2008
    {
        'year': 2008,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068322.XLS',
        'file_type': 'xls'
    },
    {
        'year': 2008,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068320.XLS',
        'file_type': 'xls'
    },
    {
        'year': 2008,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068318.XLS',
        'file_type': 'xls'
    },
    {
        'year': 2008,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068347.XLS',
        'file_type': 'xls'
    },
    {
        'year': 2008,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068345.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [64, 65, 66, 67, 68]
    },
    {
        'year': 2008,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068343.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [59, 60, 61, 62, 63, 64, 65]
    },
    {
        'year': 2008,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068339.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [51, 52, 53, 54, 55],
    },
    {
        'year': 2008,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068335.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [52, 53, 54, 55, 56],
        'fields': {
            'neighborhood': 0,
            'total': 1,
            'rape': 2,
            'robbery': 3,
            'agg_assault': 4,
            'burglary': 5,
            'larceny': 6,
            'auto_theft': 7,
            'arson': 8
        }
    },
    {
        'year': 2008,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068333.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [58, 59, 60, 61, 62, 63],
    },
    {
        'year': 2008,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068331.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [66, 67, 68, 69, 70],
    },
    {
        'year': 2008,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068329.XLS',
        'file_type': 'xls'
    },
    {
        'year': 2008,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068327.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': [50, 51, 52, 53, 54, 55],
        'fields': {
            'neighborhood': 0,
            'total': 1,
            'rape': 2,
            'robbery': 3,
            'agg_assault': 4,
            'burglary': 5,
            'larceny': 6,
            'auto_theft': 7,
            'arson': 8
        }
    },
    
    # 2007
    {
        'year': 2007,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068356.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 55 + 1),
    },
    {
        'year': 2007,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068354.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 55 + 1),
    },
    {
        'year': 2007,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068352.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 56 + 1),
    },
    {
        'year': 2007,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068350.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1),
    },
    {
        'year': 2007,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068378.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1)
    },
    {
        'year': 2007,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068376.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1)
    },
    {
        'year': 2007,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068372.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1),
    },
    {
        'year': 2007,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068370.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(49, 55 + 1)
    },
    {
        'year': 2007,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068368.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(53, 57 + 1) + [97, 98],
    },
    {
        'year': 2007,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068366.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(53, 57 + 1) + [97, 98],
    },
    {
        'year': 2007,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068362.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(53, 57 + 1) + [97, 98],
    },
    {
        'year': 2007,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068360.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [96, 97],
    },
    
    # 2006
    {
        'year': 2006,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068386.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068384.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(49, 53 + 1) + [95, 96],
    },
    {
        'year': 2006,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068382.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2006,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068412.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068410.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068408.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068404.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068402.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068399.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2006,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068397.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [98, 99],
    },
    {
        'year': 2006,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068393.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2006,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068391.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    
    # 2005
    {
        'year': 2005,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068419.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [97, 98],
    },
    {
        'year': 2005,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068417.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2005,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068415.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2005,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068451.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2005,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068444.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [97, 98],
    },
    {
        'year': 2005,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068442.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2005,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068438.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2005,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068436.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2005,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068434.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    # March 2005 Excel file missing and cannot determine it
    # from the URL.
    # http://www.minneapolismn.gov/police/statistics/WCMS1Q-068311
    #
    # TODO: Contact MPD
    #
    #{
    #    'year': 2005,
    #    'month': 3,
    #    'url': '',
    #    'file_type': 'xls',
    #    'start_row': 5,
    #    'skip_rows': range(52, 56 + 1) + [98, 99],
    #},
    {
        'year': 2005,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068427.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2005,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068425.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [95, 96],
    },
    
    # 2004
    {
        'year': 2004,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068461.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068459.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2004,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068457.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [98, 99],
    },
    {
        'year': 2004,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068455.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068453.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068475.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068473.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068471.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068469.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068467.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2004,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068465.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2004,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068463.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    
    # 2003
    {
        'year': 2003,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068486.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2003,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068483.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2003,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068482.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068480.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068478.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2003,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068476.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068498.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2003,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068496.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068494.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068492.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2003,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068490.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(50, 54 + 1) + [96, 97],
    },
    {
        'year': 2003,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/WCMS1Q-068488.XLS',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [97, 98],
    },
    
    # 2002
    {
        'year': 2002,
        'month': 12,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068511.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2002,
        'month': 11,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068509.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [98, 99],
    },
    {
        'year': 2002,
        'month': 10,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068507.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97],
    },
    {
        'year': 2002,
        'month': 9,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068505.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    {
        'year': 2002,
        'month': 8,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068503.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(52, 56 + 1) + [98, 99],
    },
    {
        'year': 2002,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068501.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98, 99],
    },
    {
        'year': 2002,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068519.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [96, 97, 98, 99],
        # Note in spreadsheet: The Homicides in Powderhorn Park and Jordan were ruled "justifiable".
    },
    # 2002 - May is missing
    {
        'year': 2002,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1q-068516.xls',
        'file_type': 'xls',
        'start_row': 5,
        'skip_rows': range(51, 55 + 1) + [97, 98],
    },
    
    # 2013
    {
        'year': 2013,
        'month': 1,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-104213.xlsx',
    },
    {
        'year': 2013,
        'month': 2,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-105285.xlsx',
    },
    {
        'year': 2013,
        'month': 3,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-106697.xlsx',
    },
    {
        'year': 2013,
        'month': 4,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-108036.xlsx',
    },
    {
        'year': 2013,
        'month': 5,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-109747.xlsx',
        'skip_rows': [86, 87]
    },
    {
        'year': 2013,
        'month': 6,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-110838.xlsx'
    },
    {
        'year': 2013,
        'month': 7,
        'url': 'http://www.minneapolismn.gov/www/groups/public/@mpd/documents/webcontent/wcms1p-112499.xlsx'
    }

    
    # Excel reports stop here
]

process_reports(reports)