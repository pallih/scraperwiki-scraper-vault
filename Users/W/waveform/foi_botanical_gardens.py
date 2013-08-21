# Created at Python Northwest, Manchester, 2010-11-15


import scraperwiki
import datetime
import xlrd

# retrieve a page
starting_url = 'http://www.mapmywalk.com/routes/view/148028007'
book = xlrd.open_workbook(file_contents=scraperwiki.scrape(starting_url))
XL_EPOCH = datetime.date(1899, 12, 30)
scraperwiki.metadata.save('data_columns', ['Date', 'tmin', 'tmax', 'tmean'])


count = 0
for sheet in book.sheets():
    print 'Scraping sheet %s' % sheet.name
    for rownum in xrange(sheet.nrows):
        date_cell = sheet.cell(rownum, 0)
        min_cell = sheet.cell(rownum, 2)
        max_cell = sheet.cell(rownum, 1)
        if date_cell.ctype == xlrd.XL_CELL_DATE and xlrd.XL_CELL_NUMBER in (min_cell.ctype, max_cell.ctype):
            record = {}
            record['Date'] = str(XL_EPOCH + datetime.timedelta(days=date_cell.value))
            if min_cell.ctype == xlrd.XL_CELL_NUMBER:
                record['tmin'] = min_cell.value
            if max_cell.ctype == xlrd.XL_CELL_NUMBER:
                record['tmax'] = max_cell.value
            if min_cell.ctype == xlrd.XL_CELL_NUMBER and max_cell.ctype == xlrd.XL_CELL_NUMBER:
                record['tmean'] = (min_cell.value + max_cell.value) / 2.0
            scraperwiki.sqlite.save(unique_keys=['Date'], data=record)
            count += 1

print 'Scraped %d records' % count