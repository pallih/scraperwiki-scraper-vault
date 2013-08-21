import xlrd    

import re
from scraperwiki import scrape

url = 'http://www.dh.gov.uk/prod_consum_dh/groups/dh_digitalassets/@dh/@en/documents/digitalasset/dh_123467.xls'

book = xlrd.open_workbook(file_contents=scrape(url))#workbook open

print "Workbook has %s sheet(s)" % book.nsheets## of sheets

for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)#row and column names

firstSheet = book.sheet_by_index(0)
                      
for row in range(0,firstSheet.nrows): 
    for column in range(0,firstSheet.ncols): 
        cell = firstSheet.cell(row,column)

        cellValue = unicode(cell.value)
        
        match = re.match("(\d{4}-\d{2,4})",cellValue)
        if match:
            print "Year: " + cellValue

                              


