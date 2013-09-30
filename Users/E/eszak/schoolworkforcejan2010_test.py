import xlrd

import re
import string
from scraperwiki import scrape

url = 'http://www.dcsf.gov.uk/rsgateway/DB/SFR/s000927/sfr11-2010-rev.xls'

book = xlrd.open_workbook(file_contents=scrape(url))

print "Workbook has %s sheet(s)" % book.nsheets

for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

import xlrd

import re
import string
from scraperwiki import scrape

url = 'http://www.dcsf.gov.uk/rsgateway/DB/SFR/s000927/sfr11-2010-rev.xls'

book = xlrd.open_workbook(file_contents=scrape(url))

print "Workbook has %s sheet(s)" % book.nsheets

for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

