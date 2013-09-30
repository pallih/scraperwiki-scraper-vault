# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html

#Most of this code has been used from Paul Bradshaw's NHS Sitrep tutorials
# https://scraperwiki.com/scrapers/excelscraper_sitreps_multiplesheets_2/

import xlrd    

import re
import string
import scraperwiki
from scraperwiki import scrape
import datetime
import time

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

try:
    scraperwiki.sqlite.execute("""
        create table gplist
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."



#set a variable for the spreadsheet location
XLS = 'https://indicators.ic.nhs.uk/download/Demography/Data/Practice%20Registered%20List%20inc%20age%20gender%20breakdown.xls'

#use the scrape function on that spreadsheet to create a new variable 'xlbin'
xlbin = scraperwiki.scrape(XLS)
#print xlbin
#use the open_workbook function on that new variable to create another, 'book'
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (15) to grab the 16th row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(16)

#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[5]

#put cells from the ... row into 'keys' variable 
keys = sheet.row_values(15)
#keys = []

record = {}
print "keys", keys

#print how many columns the sheet has
print "sheet.ncols: ", sheet.ncols
idno = 0
for rownumber in range(16, sheet.nrows):
    print "scraping row ", rownumber
    Name = "no entry"
    for num in range(0,sheet.ncols):
        print "column number:", num
        #record['title'] = title
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
        record[keys[num]] = sheet.row_values(rownumber)[num]
    idno = idno + 1
    record['id'] = str(idno)
    print "---", record
    scraperwiki.sqlite.save(unique_keys=[],data=record, table_name='gplist')
    

#spreadsheet found at 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html

#Most of this code has been used from Paul Bradshaw's NHS Sitrep tutorials
# https://scraperwiki.com/scrapers/excelscraper_sitreps_multiplesheets_2/

import xlrd    

import re
import string
import scraperwiki
from scraperwiki import scrape
import datetime
import time

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

try:
    scraperwiki.sqlite.execute("""
        create table gplist
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."



#set a variable for the spreadsheet location
XLS = 'https://indicators.ic.nhs.uk/download/Demography/Data/Practice%20Registered%20List%20inc%20age%20gender%20breakdown.xls'

#use the scrape function on that spreadsheet to create a new variable 'xlbin'
xlbin = scraperwiki.scrape(XLS)
#print xlbin
#use the open_workbook function on that new variable to create another, 'book'
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (15) to grab the 16th row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(16)

#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[5]

#put cells from the ... row into 'keys' variable 
keys = sheet.row_values(15)
#keys = []

record = {}
print "keys", keys

#print how many columns the sheet has
print "sheet.ncols: ", sheet.ncols
idno = 0
for rownumber in range(16, sheet.nrows):
    print "scraping row ", rownumber
    Name = "no entry"
    for num in range(0,sheet.ncols):
        print "column number:", num
        #record['title'] = title
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
        record[keys[num]] = sheet.row_values(rownumber)[num]
    idno = idno + 1
    record['id'] = str(idno)
    print "---", record
    scraperwiki.sqlite.save(unique_keys=[],data=record, table_name='gplist')
    

#spreadsheet found at 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'