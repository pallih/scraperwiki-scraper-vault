# This is Rob's first attempt at biting off more than he can chew
# DoH 18w RTT stats scraper

# rewired state hacklab event 26th march

# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
import string
from scraperwiki import scrape
from scraperwiki import datastore

# Let's grab the Referral to Treatment Waiting Times Statistics from the DoH
# http://tinyurl.com/49xns44
# Looking at January 2011 Commissioner Data Adjusted Admitted Pathways
url = 'http://www.dh.gov.uk/dr_consum_dh/groups/dh_digitalassets/@dh/@en/@ps/@sta/@perf/documents/digitalasset/dh_125182.xls'
filename = 'dh_125182'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
#for sheet in book.sheets():
#    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can also access each worksheet by its index
# Select a sheet
sh = book.sheet_by_index(0)
firstSheet = book.sheet_by_index(0)

# for sheet in book.sheets():

headers = firstSheet.row(13)

# grab data from rows 14-34
for row in range(14,33): # for each row
#    for column in range(1,63): # for each column within the row
#        cell = firstSheet.cell(row,column)

    row_values = dict(zip([str(h.value) for h in headers], [str(v.value) for v in firstSheet.row(row)]))

    del row_values['']
    for k,v in row_values.items():
        clean_key = re.sub(r'\(|\)|\>|\<', '', k)
        print clean_key
        row_values[clean_key] = v
        
    row_values['filename'] = "%s--%s--%s" % (filename, sh.name, firstSheet.row(row)[1].value)
    print row_values.keys()
    datastore.save(['filename',], row_values)
# This is Rob's first attempt at biting off more than he can chew
# DoH 18w RTT stats scraper

# rewired state hacklab event 26th march

# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
import string
from scraperwiki import scrape
from scraperwiki import datastore

# Let's grab the Referral to Treatment Waiting Times Statistics from the DoH
# http://tinyurl.com/49xns44
# Looking at January 2011 Commissioner Data Adjusted Admitted Pathways
url = 'http://www.dh.gov.uk/dr_consum_dh/groups/dh_digitalassets/@dh/@en/@ps/@sta/@perf/documents/digitalasset/dh_125182.xls'
filename = 'dh_125182'

# This line will open the spreasheet from an url
book = xlrd.open_workbook(file_contents=scrape(url))

# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

# Loop over each sheet, print name, and number of rows/colums
#for sheet in book.sheets():
#    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can also access each worksheet by its index
# Select a sheet
sh = book.sheet_by_index(0)
firstSheet = book.sheet_by_index(0)

# for sheet in book.sheets():

headers = firstSheet.row(13)

# grab data from rows 14-34
for row in range(14,33): # for each row
#    for column in range(1,63): # for each column within the row
#        cell = firstSheet.cell(row,column)

    row_values = dict(zip([str(h.value) for h in headers], [str(v.value) for v in firstSheet.row(row)]))

    del row_values['']
    for k,v in row_values.items():
        clean_key = re.sub(r'\(|\)|\>|\<', '', k)
        print clean_key
        row_values[clean_key] = v
        
    row_values['filename'] = "%s--%s--%s" % (filename, sh.name, firstSheet.row(row)[1].value)
    print row_values.keys()
    datastore.save(['filename',], row_values)
