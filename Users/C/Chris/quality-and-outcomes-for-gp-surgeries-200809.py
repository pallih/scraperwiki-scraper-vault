### Basic QOF scraper
# Imports Quality and Outcomes for GP surgeries. The data is already available in a reasonable format, we just import it to ScraperWiki.
# We import the practice level data tables and practice level prevalence tables.

### Data & Copyright details:
#Data source: QMAS database - 2008/09 data as at end of June 2009
#SHA and PCT codes are used for administrative purposes in local and national databases
#For PMS practices participating in the national QOF, achieved points shown are prior to PMS points deductions.
#This work remains the sole and exclusive property of the Health and Social Care Information Centre and may only be reproduced where 
#there is explicit reference to the ownership of the Health and Social Care Information Centre.
#This work may be re-used by NHS and government organisations without permission.
#This work is subject to the Re-Use of Public Sector Information Regulations and permission for commercial use must be obtained from the copyright holder.
#Copyright © 2009, The Health and Social Care Information Centre, Prescribing Support Unit. All rights reserved.

### Additional Notes (correct for data tables downloaded on 26 August 2010)

# For Age-Specific Prevalence data the prevalence figures calculated for practices with codes Y02442, Y02164, C81105, C81050, B82087 use the national proportions of patients aged 16+, 17+ and 18+.

# The following practices were not included in the QOF publication dataset taken from the QMAS at the end of June 2009. The information below was supplied by PCTs:
#SHA    SHA Name    PCT    PCT Name    Practice    Notes supplied by PCTs
#Q32    YORKSHIRE AND THE HUMBER STRATEGIC HEALTH AUTHORITY    5N1    LEEDS PCT    B86074    This practice achieved 996.81 points in 2008/09. Clinical domain 648.33; Organisational domain 165.98; Patient Experience domain 146.5; Additional Services domain 36.
#Q36    LONDON STRATEGIC HEALTH AUTHORITY    5HX    EALING PCT    E85049    This practice's QOF achievement was subject to sign-off in September 2009. Its forecast achievement was 895.5 points: Clinical domain 612; Organisational domain 159.5; Patient Experience domain 88; Additional Services domain 36.
#Q36    LONDON STRATEGIC HEALTH AUTHORITY    5C9    HARINGEY PCT    F85028    This practice achieved 885.45 points in 2008/09. Clinical domain 598.41; Organisational domain 162.83; Patient Experience domain 91.65; Additional Services domain 32.56.
#Q31    NORTH WEST STRATEGIC HEALTH AUTHORITY    5NR    TRAFFORD PCT    P91021    This practice achieved 985.61 points in 2008/09.

from xlrd import open_workbook
from lxml import html
import scraperwiki

# Global data
headings_row = 13
datatables = 'http://www.ic.nhs.uk/default.asp?sID=1253285481231'

prevalencetable = 'http://www.ic.nhs.uk/webfiles/QOF/2008-09/Prevalence%20tables/QOF0809_Pracs_Prevalence.xls'
commonheadings = ['SHA Code', 'Strategic Health Authority Name', 'PCT Code', 'PCT Name', 'Practice Code', 'Practice Name']

def mergedata(data, d):
    for key in d.iterkeys():
        if data.has_key(key):
            data[key].update(d[key])
        else:
            data[key] = d[key]
    return data
    
def scrape_sheet(s, prefix):
    headings = {}
    for col in range(s.ncols):
        heading = s.cell(headings_row, col).value
        if heading:
            if heading in commonheadings:
                headings[col] = heading
            else:
                headings[col] = prefix + heading
    data = {}
    print 'Found data:', headings
    for row in range(headings_row + 1, s.nrows):
        e = {}
        if not s.cell(row, 0).value:
            break
        for col in range(s.ncols):
            if headings.has_key(col):
                e[headings[col]] = s.cell(row, col).value
        data[tuple(map(e.get, commonheadings))] = e
    return data

def scrape_book(filedata, prefix):
    wb = open_workbook(file_contents = filedata)
    data = {}
    prefix2 = prefix
    for s in wb.sheets():
        if s.name != 'QOF export':
            prefix2 = prefix + s.name + ' - '
        else:
            prefix2 = prefix
        data = mergedata(data, scrape_sheet(s, prefix2))
    return data

def getdomains(xhtml):
    root = html.fromstring(xhtml, parser = html.xhtml_parser)
    root.resolve_base_href()
    ns = '{%s}' % root.nsmap[None]
    data = {}
    for a in root.iter(ns + 'a'):
        if a.get('href').endswith('.xls'):
            prefix = a.text.split('(xls')[0].split('2008/09 - ')[1] + '- '
            print "Fetching file..."
            xls = scraperwiki.scrape(a.get('href'))
            print "Scraping file..."
            data = mergedata(data, scrape_book(xls, prefix))
    return data

def main():
    data = getdomains(scraperwiki.scrape(datatables))
    print "Fetching prevalence table..."
    prev = scrape_book(scraperwiki.scrape(prevalencetable), 'prevalence - ')
    data = mergedata(data, prev)
    print "Obtained " + str(len(data)) + " records. Saving..."
    for record in data.itervalues():
        scraperwiki.datastore.save(unique_keys = commonheadings, data = record, silent = True)

main()


