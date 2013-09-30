# Code rudely borrowed from
# http://scraperwiki.com/scrapers/foi_botanical_gardens/

import scraperwiki
import datetime
import xlrd

# retrieve a page
starting_url = 'http://www.whatdotheyknow.com/request/49503/response/132083/attach/4/Kew%20Gardens%20Max%20Mins.XLS.xls'
book = xlrd.open_workbook(file_contents=scraperwiki.scrape(starting_url))
# XL_EPOCH = datetime.date(1899, 12, 30)
# scraperwiki.metadata.save('data_columns', ['Date', 'tmin', 'tmax', 'tmean'])

scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS swdata (id text, element text, date text, v real)""")

print book.datemode
count = 0
stationid = 'uk_kew'
date='no date yet'
# We only expect 1 sheet, but we iterate through them anyway.
for sheet in book.sheets():
    print 'Scraping sheet %s' % sheet.name
    # Each row gives a min and max observation, there are 2 a day (0900, 2100 GMT).
    # We use the morning's min as the day's min, and the evening's max as the day's max.
    for rownum in xrange(sheet.nrows):
        if rownum % 100 == 0:
            print rownum, date, sheet.row(rownum)
        date_cell = sheet.cell(rownum, 0)
        max_cell = sheet.cell(rownum, 1)
        min_cell = sheet.cell(rownum, 2)
        records = []
        if date_cell.ctype == xlrd.XL_CELL_DATE and xlrd.XL_CELL_NUMBER in (min_cell.ctype, max_cell.ctype):
            record = {}
            datetime_tuple = xlrd.xldate_as_tuple(date_cell.value, book.datemode)
            time_triple = datetime_tuple[3:]
            if time_triple < (12,0,0):
                record['element'] = 'tminD'
                v = min_cell.value
            else:
                record['element'] = 'tmaxD'
                v = max_cell.value
            date = "%04d-%02d-%02d" % datetime_tuple[:3]
            record['date'] = date
            record['id'] = stationid
            record['v'] = v
            records.append(record)
            count += 1

        scraperwiki.sqlite.save(['id', 'element', 'date'], records, verbose=0)

print 'Scraped %d records' % count# Code rudely borrowed from
# http://scraperwiki.com/scrapers/foi_botanical_gardens/

import scraperwiki
import datetime
import xlrd

# retrieve a page
starting_url = 'http://www.whatdotheyknow.com/request/49503/response/132083/attach/4/Kew%20Gardens%20Max%20Mins.XLS.xls'
book = xlrd.open_workbook(file_contents=scraperwiki.scrape(starting_url))
# XL_EPOCH = datetime.date(1899, 12, 30)
# scraperwiki.metadata.save('data_columns', ['Date', 'tmin', 'tmax', 'tmean'])

scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS swdata (id text, element text, date text, v real)""")

print book.datemode
count = 0
stationid = 'uk_kew'
date='no date yet'
# We only expect 1 sheet, but we iterate through them anyway.
for sheet in book.sheets():
    print 'Scraping sheet %s' % sheet.name
    # Each row gives a min and max observation, there are 2 a day (0900, 2100 GMT).
    # We use the morning's min as the day's min, and the evening's max as the day's max.
    for rownum in xrange(sheet.nrows):
        if rownum % 100 == 0:
            print rownum, date, sheet.row(rownum)
        date_cell = sheet.cell(rownum, 0)
        max_cell = sheet.cell(rownum, 1)
        min_cell = sheet.cell(rownum, 2)
        records = []
        if date_cell.ctype == xlrd.XL_CELL_DATE and xlrd.XL_CELL_NUMBER in (min_cell.ctype, max_cell.ctype):
            record = {}
            datetime_tuple = xlrd.xldate_as_tuple(date_cell.value, book.datemode)
            time_triple = datetime_tuple[3:]
            if time_triple < (12,0,0):
                record['element'] = 'tminD'
                v = min_cell.value
            else:
                record['element'] = 'tmaxD'
                v = max_cell.value
            date = "%04d-%02d-%02d" % datetime_tuple[:3]
            record['date'] = date
            record['id'] = stationid
            record['v'] = v
            records.append(record)
            count += 1

        scraperwiki.sqlite.save(['id', 'element', 'date'], records, verbose=0)

print 'Scraped %d records' % count