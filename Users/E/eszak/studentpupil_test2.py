import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://www.education.gov.uk/rsgateway/DB/SFR/s001030/sfr25-2011ntv2.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_index(0)
sheet = book.sheet_by_name('Table 1')


print "Workbook has %s sheet(s)" % book.nsheets

for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

print sheet.row_values(4)           

import datetime
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

print [ cellval(c, book.datemode) for c in sheet.row(4) ]           

print cellval(sheet.cell(0,0))