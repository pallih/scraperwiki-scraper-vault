###############################################################################
# Scraper for data from University of Cambridge Botanical Gardens
# http://www.whatdotheyknow.com/request/temperature_data_from_botanical
###############################################################################

import datetime
import scraperwiki
import xlrd

data_uri = 'http://www.whatdotheyknow.com/request/49024/response/124689/attach/3/FOI%202010%20207%20Jones.xls'

def xldate_as_isodate(date, datemode):
    datetuple = xlrd.xldate_as_tuple(date, datemode)
    dt = datetime.datetime(*datetuple)
    return dt.date().isoformat()    

def scrape_worksheet(worksheet):
    # Columns are Date, Max, Min
    # The first and third rows contain headings
    # There is a summary containing averages and totals for each month
    # Assume each row with a date on it also contains the temperatures
    records = []
    for row in range(worksheet.nrows):
        celltype = worksheet.cell_type(rowx=row, colx=0);
        
        if (celltype == xlrd.XL_CELL_DATE):
            xldate = worksheet.cell_value(rowx=row, colx=0)
            isodate = xldate_as_isodate(xldate, book.datemode)
            maxtemp = worksheet.cell_value(rowx=row, colx=1)
            mintemp = worksheet.cell_value(rowx=row, colx=2)
            records.append({ 'date': isodate, 'tmax': maxtemp, 'tmin': mintemp })
    
    return records

def scrape_workbook(workbook):
    # The workbook contains one sheet for each year of data
    print "The workbookbook has %d sheets" % (workbook.nsheets,)
    for sheet in workbook.sheets():
        print "Sheet %s has %d rows" % (sheet.name, sheet.nrows)
        records = scrape_worksheet(sheet)
        scraperwiki.sqlite.save(unique_keys=['date'], data=records)

# Retrieve the data
xls = scraperwiki.scrape(data_uri)
book = xlrd.open_workbook(file_contents=xls)
scrape_workbook(book)###############################################################################
# Scraper for data from University of Cambridge Botanical Gardens
# http://www.whatdotheyknow.com/request/temperature_data_from_botanical
###############################################################################

import datetime
import scraperwiki
import xlrd

data_uri = 'http://www.whatdotheyknow.com/request/49024/response/124689/attach/3/FOI%202010%20207%20Jones.xls'

def xldate_as_isodate(date, datemode):
    datetuple = xlrd.xldate_as_tuple(date, datemode)
    dt = datetime.datetime(*datetuple)
    return dt.date().isoformat()    

def scrape_worksheet(worksheet):
    # Columns are Date, Max, Min
    # The first and third rows contain headings
    # There is a summary containing averages and totals for each month
    # Assume each row with a date on it also contains the temperatures
    records = []
    for row in range(worksheet.nrows):
        celltype = worksheet.cell_type(rowx=row, colx=0);
        
        if (celltype == xlrd.XL_CELL_DATE):
            xldate = worksheet.cell_value(rowx=row, colx=0)
            isodate = xldate_as_isodate(xldate, book.datemode)
            maxtemp = worksheet.cell_value(rowx=row, colx=1)
            mintemp = worksheet.cell_value(rowx=row, colx=2)
            records.append({ 'date': isodate, 'tmax': maxtemp, 'tmin': mintemp })
    
    return records

def scrape_workbook(workbook):
    # The workbook contains one sheet for each year of data
    print "The workbookbook has %d sheets" % (workbook.nsheets,)
    for sheet in workbook.sheets():
        print "Sheet %s has %d rows" % (sheet.name, sheet.nrows)
        records = scrape_worksheet(sheet)
        scraperwiki.sqlite.save(unique_keys=['date'], data=records)

# Retrieve the data
xls = scraperwiki.scrape(data_uri)
book = xlrd.open_workbook(file_contents=xls)
scrape_workbook(book)