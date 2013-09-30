# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    
import re
import string
import scraperwiki
from scraperwiki import scrape

url = 'http://www.artscouncil.org.uk/media/uploads/portfolio_spreadsheets/national_portfolio_organisations_30_march_2011.xls'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# We can find out information about the workbook - number of sheets
#print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can also access each worksheet by its index
sheet = book.sheet_by_index(0)
headers = []
for column in range(0,sheet.ncols): 
    cell = sheet.cell(0,column)
    cellValue = unicode(cell.value)
    headers.append(cellValue.replace('?','').replace('%','percent').replace('(','-').replace(')','-').replace('/','-'))
    #print headers                      
# You can loop over all the cells in the worksheet
for r in range(1,sheet.nrows-2):
    row = []
    for column in range(0,sheet.ncols): # for each column within the row
        cell = sheet.cell(r,column)
        cellValue = cell.value
        if cellValue == 'Visual arts':
            cellValue = 'Visual Arts'
        if cellValue == 'Visual arts ':
            cellValue = 'Visual Arts'
        if type(cellValue) in [str, unicode]:
            cellValue = cellValue.strip()
        row.append(cellValue)
    #print row
    data = dict(zip(headers, row))
    print data
    #scraperwiki.datastore.save(unique_keys=['Name'], data=data)  
        
       

# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    
import re
import string
import scraperwiki
from scraperwiki import scrape

url = 'http://www.artscouncil.org.uk/media/uploads/portfolio_spreadsheets/national_portfolio_organisations_30_march_2011.xls'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# We can find out information about the workbook - number of sheets
#print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can also access each worksheet by its index
sheet = book.sheet_by_index(0)
headers = []
for column in range(0,sheet.ncols): 
    cell = sheet.cell(0,column)
    cellValue = unicode(cell.value)
    headers.append(cellValue.replace('?','').replace('%','percent').replace('(','-').replace(')','-').replace('/','-'))
    #print headers                      
# You can loop over all the cells in the worksheet
for r in range(1,sheet.nrows-2):
    row = []
    for column in range(0,sheet.ncols): # for each column within the row
        cell = sheet.cell(r,column)
        cellValue = cell.value
        if cellValue == 'Visual arts':
            cellValue = 'Visual Arts'
        if cellValue == 'Visual arts ':
            cellValue = 'Visual Arts'
        if type(cellValue) in [str, unicode]:
            cellValue = cellValue.strip()
        row.append(cellValue)
    #print row
    data = dict(zip(headers, row))
    print data
    #scraperwiki.datastore.save(unique_keys=['Name'], data=data)  
        
       

