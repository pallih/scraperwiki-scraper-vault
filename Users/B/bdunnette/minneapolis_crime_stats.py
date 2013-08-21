import scraperwiki           
import xlrd
import datetime
import calendar
import lxml.html

sources = []
pages = ["http://www.minneapolismn.gov/police/statistics/WCMS1Q-068308", "http://www.minneapolismn.gov/police/statistics/crime-statistics_codefor_statistics", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068309", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-067125", "http://www.minneapolismn.gov/police/statistics/WCMS1P-087449", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-067319", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068310", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068311", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068312", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068313", "http://www.minneapolismn.gov/police/statistics/WCMS1Q-068314"]

for page in pages:
    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)
    for a in root.cssselect("table a"):
        filename = a.attrib['href']
        if filename.upper().endswith('.XLS'):
            sources.append({'date': a.text, 'url': 'http://www.minneapolismn.gov/' + filename})

print sources
for source in sources:
    print 'Parsing ' + source['url']
    xlbin = scraperwiki.scrape(source['url'])
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)           
    
    keys = sheet.row_values(0)
    start_row = 1
    #check for old-style sheets, which have four-row header before data
    if 'MINNEAPOLIS' in keys[0]:
        keys = sheet.row_values(4)    
        start_row = 5
    print keys
    for key in keys:
        keys[keys.index(key)] = key.strip().replace('.','').replace(' ','').capitalize().rstrip('s')
    
    if 'Neig' in keys[0]:
        print 'Sheet Name: ' + sheet.name
        if len(sheet.name.split()) == 2:
            year = sheet.name.split()[1]
            month = list(calendar.month_name).index(sheet.name.split()[0])
        elif source['date']:
            print 'Unable to get date from sheet name, falling back to link title (%s)' % source['date']
            month_name = source['date'].split()[0]
            if month_name in calendar.month_name:
                month = list(calendar.month_name).index(month_name)
            elif month_name in calendar.month_abbr:
                month = list(calendar.month_abbr).index(month_name)
            year = source['date'].rsplit(' ',1)[1]
        
        if month and year:
            for row_num in range(start_row, sheet.nrows):
                row = sheet.row(row_num)
                values = [ c.value for c in row ]
                if (values[1] != '') and ('Neig' not in values[0]):
                    #print values
                    row_data = dict(zip(keys, values))
                    for misspelling in ['Neigborhood', 'Neighborhhood']:
                        if misspelling in row_data:
                            row_data['Neighborhood'] = row_data[misspelling]
                            del row_data[misspelling]
                    row_data['Neighborhood'] = row_data['Neighborhood'].upper()
                    row_data['Month'] = month
                    row_data['Year'] = year
                    scraperwiki.sqlite.save(unique_keys=['Neighborhood','Year','Month'], data=row_data)