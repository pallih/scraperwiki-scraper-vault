import scraperwiki
import urllib2
import xlrd

url = "http://www.whatdotheyknow.com/request/49869/response/128432/attach/3/sw%20climate%20sitelisting.xls"

raw = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=raw)

sheet = book.sheets()[0]

def sheet_rows(sheet):
    for i in range(sheet.nrows):
        row = sheet.row(i)
        yield row

def remove_blanks(rows):
    for row in rows:
        if row[11].value:
            yield row

for i,row in enumerate(remove_blanks(sheet_rows(sheet))):
    if row[0].value.lower() == 'region':
        # ignore first row: header line
        continue
    if row[0].value:
        # Size is dubious.  Don't know if anything appears in Column E.
        d = dict(zip(['Region', 'Area', 'Ref', 'SiteName', 'E', 'SiteType', 'Status', 'GridRef', 'Catchment', 'Size', 'Location', 'Para', 'M', 'Availability'],[cell.value for cell in row]))
    else:
        d['Para'] = row[11].value
        d['Availability'] = row[13].value
    scraperwiki.sqlite.save(['Ref', 'Para'], data=d, verbose=2*(not i%10))
    
