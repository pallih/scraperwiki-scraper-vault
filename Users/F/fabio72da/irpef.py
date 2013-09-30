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



# Nice example of a spreadsheet with useful data!
url = 'http://www.finanze.gov.it/dipartimentopolitichefiscali/fiscalitalocale/distribuz_addirpef/download/H501.xls?20110307151309'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# list column names
colnames= ["IRPEF","anno","comune","range","num","tot"]

# define column names
scraperwiki.metadata.save('data_columns', colnames)


# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

    # You can also access each worksheet by its index
    #firstSheet = book.sheet_by_index(0)
    
    #pre-set data storage vector
    record = {}
    record['IRPEF']='IRPEF'
    
    # You can loop over all the cells in the worksheet
    for row in range(0,sheet.nrows): # for each row
    
        # Test (current row, 1st col) to see if it's a range
        match =re.search(".000",unicode(sheet.cell(row,0)))
        if match:
            print "Range: " + unicode(sheet.cell(row,0))
            record["anno"] = sheet.name[-4:]
            record["comune"] = sheet.name[1:4]
            i=0
            for column in range(0,sheet.ncols): # for each column within the row
                cell = sheet.cell(row,column)
    
                # Each cell may contain unicode
                cellValue = unicode(cell.value)
            
                if cellValue != "":
                    record[colnames[i+3]] = cellValue
                    i=i+1
    
    
            # Print out the data we've gathered
            print record, '------------'
                
            # We could then extract the income tax rates by year.
            scraperwiki.datastore.save(["IRPEF"], record)
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



# Nice example of a spreadsheet with useful data!
url = 'http://www.finanze.gov.it/dipartimentopolitichefiscali/fiscalitalocale/distribuz_addirpef/download/H501.xls?20110307151309'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# list column names
colnames= ["IRPEF","anno","comune","range","num","tot"]

# define column names
scraperwiki.metadata.save('data_columns', colnames)


# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

    # You can also access each worksheet by its index
    #firstSheet = book.sheet_by_index(0)
    
    #pre-set data storage vector
    record = {}
    record['IRPEF']='IRPEF'
    
    # You can loop over all the cells in the worksheet
    for row in range(0,sheet.nrows): # for each row
    
        # Test (current row, 1st col) to see if it's a range
        match =re.search(".000",unicode(sheet.cell(row,0)))
        if match:
            print "Range: " + unicode(sheet.cell(row,0))
            record["anno"] = sheet.name[-4:]
            record["comune"] = sheet.name[1:4]
            i=0
            for column in range(0,sheet.ncols): # for each column within the row
                cell = sheet.cell(row,column)
    
                # Each cell may contain unicode
                cellValue = unicode(cell.value)
            
                if cellValue != "":
                    record[colnames[i+3]] = cellValue
                    i=i+1
    
    
            # Print out the data we've gathered
            print record, '------------'
                
            # We could then extract the income tax rates by year.
            scraperwiki.datastore.save(["IRPEF"], record)
