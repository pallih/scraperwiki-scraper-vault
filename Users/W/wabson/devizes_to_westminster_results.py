import scraperwiki
import re
import urllib2
import lxml.html

from datetime import date

data = { 'locations': [], 'class_results': [], 'subclass_results': [] }
batch_size = 1000

base_url = 'http://www.dwrace.org.uk/results'

# NOT USED
keys = {
    'class_results': [ 'year', 'boat_number', 'surname_1', 'forename_1', 'gender_1', 'club_1', 'surname_2', 'forename_2', 'gender_2', 'club_2', 'time_adjustment', 'tunnel_elapsed', 'time_elapsed', 'position', 'notes', 'retired' ],
    'subclass_results': [ 'year', 'boat_number', 'surname_1', 'forename_1', 'gender_1', 'club_1', 'surname_2', 'forename_2', 'gender_2', 'club_2', 'time_adjustment', 'tunnel_elapsed', 'time_elapsed', 'position', 'notes', 'retired' ],
    'locations': [ 'year', 'boat_number', 'time_devizes', 'time_pewsey', 'time_hford', 'time_newbury', 'time_aldermaston', 'time_reading', 'time_marsh', 'time_marlow', 'time_bray', 'time_windsor', 'time_shepperton', 'time_teddington', 'time_westminster', 'status', 'time_so_far', 'notes' ]
}

unique_keys = {
    'class_results': [ 'boat_number', 'year' ],
    'subclass_results': [ 'boat_number', 'year' ],
    'locations': [ 'boat_number', 'year' ]
}

table_names = {
    'locations': 'locations',
    'class_results': 'class_results',
    'subclass_results': 'subclass_results'
}

data_verbose=0

def main():
    for year in range(2013, 2014):
        data['locations'] = []
        data['class_results'] = []
        data['subclass_results'] = []
        scrape_class_results(year)
        scrape_subclass_results(year)
        scrape_locations_overnight(str(year))

def scrape_subclass_results(year):
    print "Scraping subclass results for %s" % (year)
    results_url = '%s/%s/Results/OverallSubClassResults.html' % (base_url, year)
    try:
        results_html = lxml.html.fromstring(scraperwiki.scrape(results_url))
        class_name = None
        h1_el = results_html.find('body/h2')
        for table_el in results_html.cssselect('table'):
            entry_row = None
            table_headings = []
            # getprevious() should return h3 but actually returns the a element before the h3, since the anchor element is not closed
            if table_el.getprevious().tag == 'h3':
                class_name = table_el.getprevious().text_content().strip()
            elif table_el.getprevious().tag == 'a':
                class_name = table_el.getprevious().get('name').strip()
            caption_els = table_el.cssselect('caption')
            if len(caption_els) == 1:
                subclass_name = caption_els[0].text_content().strip()
            else:
                'Could not find class name (caption) in results table, skipping'
                continue

            if class_name is None or subclass_name is None:
                print 'Class name and subclass name are required'
                exit()

            for th_el in table_el.cssselect('tr th'):
                table_headings.append(th_el.text_content().strip())
            for r_tr_el in table_el.cssselect('tr')[1:]:
                r_td_els = r_tr_el.cssselect('td')
                if len(r_td_els) != len(table_headings):
                    print 'Results table row does not have required length %s, skipping' % (len(table_headings))
                    continue
                row_data = dict(zip(table_headings, [re.sub(r'&nbsp;?', '', d.text_content().strip()) for d in r_td_els]))

                boat_num = row_data['Number']
                surname = row_data['Surname']
                firstname = row_data['First Name']
                gender = row_data['Gender'] if 'Gender' in row_data else None
                club = row_data['Club']
                time_offset = row_data['+/- Time']
                tunnel_offset = row_data['Tunnel'] if 'Tunnel' in row_data else None
                elapsed_time = row_data['Elapsed time']
                position = row_data['Position']
                notes = row_data['Notes']

                rtd = False
                if elapsed_time.startswith('rtd'):
                    rtd = True
                dsq = False
                if elapsed_time.startswith('dsq'):
                    dsq = True

                if boat_num is not None and boat_num != '':
                    if entry_row is not None: # Save the last item
                        save_data(items={'subclass_results': entry_row})
                        entry_row = None
                    entry_row = dict([('boat_number', boat_num), ('surname_1', surname), ('firstname_1', firstname), ('gender_1', gender), ('club_1', club), ('time_offset', time_offset), ('tunnel_offset', tunnel_offset), ('elapsed_time', elapsed_time), ('retired', rtd), ('disqualified', dsq), ('subclass_position', position), ('notes', notes), ('class_name', class_name), ('subclass_name', subclass_name), ('year', year)])
                else:
                    if entry_row is not None:
                        if 'surname_2' not in entry_row and 'firstname_2' not in entry_row and 'gender_2' not in entry_row and 'club_2' not in entry_row:
                            entry_row['surname_2'] = surname
                            entry_row['firstname_2'] = firstname
                            entry_row['gender_2'] = gender
                            entry_row['club_2'] = club
                        else:
                            print 'ERROR: Found second crew member detail but there was already data present'
                            continue
                    else:
                        print 'ERROR: Found second crew member detail but no current entry object was found'
                        continue


                if 'surname_1' not in entry_row or 'firstname_1' not in entry_row or 'gender_1' not in entry_row or 'club_1' not in entry_row:
                    print("Mandatory result data was not found, skipping row")
                    continue

            # Save result data if there is still an uncommitted item
            save_data(items={'subclass_results': entry_row})
            entry_row = None

            # Flush all results in this division and the race itself to the datastore
            print "Saving %s subclass results for %s %s" % (len(data['subclass_results']), class_name, subclass_name)
            save_data({'subclass_results': None}, force=True)
            data['subclass_results'] = []
        
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing subclass data for %s' % (race_name)
        else:
            raise e

# Update position only since we should have all the other details already
def scrape_class_results(year):
    print "Scraping overall class results for %s" % (year)
    results_url = '%s/%s/Results/OverallClassResults.html' % (base_url, year)
    try:
        results_html = lxml.html.fromstring(scraperwiki.scrape(results_url))
        class_name = None
        h1_el = results_html.find('body/h2')
        for table_el in results_html.cssselect('table'):
            entry_row = None
            table_headings = []
            caption_els = table_el.cssselect('caption')
            if len(caption_els) == 1:
                class_name = caption_els[0].text_content().strip()
            else:
                'Could not find class name (caption) in results table, skipping'
                continue

            if class_name is None:
                print 'Class name is required'
                exit()

            for th_el in table_el.cssselect('tr th'):
                table_headings.append(th_el.text_content().strip())
            for r_tr_el in table_el.cssselect('tr')[1:]:
                r_td_els = r_tr_el.cssselect('td')
                if len(r_td_els) != len(table_headings):
                    print 'Results table row does not have required length %s, skipping' % (len(table_headings))
                    continue
                row_data = dict(zip(table_headings, [re.sub(r'&nbsp;?', '', d.text_content().strip()) for d in r_td_els]))

                boat_num = row_data['Number']
                surname = row_data['Surname']
                firstname = row_data['First Name']
                gender = row_data['Gender'] if 'Gender' in row_data else None
                club = row_data['Club']
                time_offset = row_data['+/- Time']
                tunnel_offset = row_data['Tunnel'] if 'Tunnel' in row_data else None
                elapsed_time = row_data['Elapsed time']
                position = row_data['Position']
                notes = row_data['Notes']

                rtd = False
                if elapsed_time.startswith('rtd'):
                    rtd = True
                dsq = False
                if elapsed_time.startswith('dsq'):
                    dsq = True

                if boat_num is not None and boat_num != '':
                    if entry_row is not None: # Save the last item
                        save_data(items={'class_results': entry_row})
                        entry_row = None
                    entry_row = dict([('boat_number', boat_num), ('surname_1', surname), ('firstname_1', firstname), ('gender_1', gender), ('club_1', club), ('time_offset', time_offset), ('tunnel_offset', tunnel_offset), ('elapsed_time', elapsed_time), ('retired', rtd), ('disqualified', dsq), ('class_position', position), ('notes', notes), ('class_name', class_name), ('year', year)])
                else:
                    if entry_row is not None:
                        if 'surname_2' not in entry_row and 'firstname_2' not in entry_row and 'gender_2' not in entry_row and 'club_2' not in entry_row:
                            entry_row['surname_2'] = surname
                            entry_row['firstname_2'] = firstname
                            entry_row['gender_2'] = gender
                            entry_row['club_2'] = club
                        else:
                            print 'ERROR: Found second crew member detail but there was already data present'
                            continue
                    else:
                        print 'ERROR: Found second crew member detail but no current entry object was found'
                        continue


                if 'surname_1' not in entry_row or 'firstname_1' not in entry_row or 'gender_1' not in entry_row or 'club_1' not in entry_row:
                    print("Mandatory result data was not found, skipping row")
                    continue

            # Save result data if there is still an uncommitted item
            save_data(items={'class_results': entry_row})
            entry_row = None

            # Flush all results in this division and the race itself to the datastore
            print "Saving %s class results for %s" % (len(data['class_results']), class_name)
            save_data({'class_results': None}, force=True)
            data['class_results'] = []
        
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing class data for %s' % (race_name)
        else:
            raise e

def scrape_locations_overnight(year):
    locations_cols = [ 'boat_number', 'status', 'time_so_far', 'notes', 'time_devizes', 'time_pewsey', 'time_hford', 'time_newbury', 'time_aldermaston', 'time_reading', 'time_marsh', 'time_marlow', 'time_bray', 'time_windsor', 'time_shepperton', 'time_teddington', 'time_westminster' ]
    locations_url = '%s/%s/Progress/OvernightPs.js' % (base_url, year)
    pattern = re.compile('OvernightPs\[([0-9]+)\]\[([0-9]+)\]=\\\'(.+)\\\'')
    countPattern = re.compile('countOvernightPs = ([0-9]+);')
    try:
        locations_js = scraperwiki.scrape(locations_url)
        m = re.search(countPattern, locations_js)
        if m is not None:
            locations_array = [[''] * 17 for f in range(int(m.group(1)))]
        else:
            print 'ERROR: No count found!'
            return
        #print locations_js
        lines = locations_js.splitlines()
        for line in lines:
            m = pattern.match(line.strip())
            if m is not None:
                i1 = int(m.group(1))
                i2 = int(m.group(2))
                val = m.group(3)
                locations_array[i1][i2] = val

        for arr_item in locations_array:
            location = dict(zip(locations_cols, arr_item))
            location['year'] = year
            save_data({'locations': location })

        # Flush all results in this division and the race itself to the datastore
        print "Saving %s location results for %s" % (len(data['locations']), year)
        save_data({'locations': None}, force=True)
                
    except urllib2.HTTPError, e:
        if e.code == 404:
            print 'WARNING: Missing position data for %s' % (year)
        else:
            raise e

# Save the data in batches
def save_data(items={}, force=False):
    global data
    for k in items.keys():
        if items[k] is not None:
            data[k].append(items[k])
        if len(data[k]) >= batch_size or force == True:
            scraperwiki.sqlite.save(unique_keys=unique_keys[k], data=data[k], table_name=table_names[k], verbose=data_verbose)
            data[k] = []
main()

