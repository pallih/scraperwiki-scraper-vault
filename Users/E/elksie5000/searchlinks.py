import scraperwiki
import lxml.html
import xlrd    
import re
import string
from scraperwiki import scrape

#scrape search page
base_url = 'http://www.ons.gov.uk'
html = scraperwiki.scrape('http://www.ons.gov.uk/ons/datasets-and-tables/index.html?pageSize=50&sortBy=none&sortDirection=none&newquery=jsa01&content-type=Reference+table&content-type=Dataset')


searchtable = lxml.html.fromstring(html)#turn html into lxml object

#identify this month and last month's spreadsheet
thismonth = searchtable.cssselect('table td a')[0]
lastmonth = searchtable.cssselect('table td a')[1]
#extract the relative URL...
thismonth = str(thismonth.xpath('@href')[0])
lastmonth = str(lastmonth.xpath('@href')[0])
#convert into a full URL
thismonth = base_url+thismonth
lastmonth = base_url+lastmonth

#open spreadsheets
book_thismonth = xlrd.open_workbook(file_contents=scrape(thismonth))
book_lastmonth = xlrd.open_workbook(file_contents=scrape(lastmonth))

# You can also access each worksheet by its index
firstSheet_thismonth = book_thismonth.sheet_by_index(0)
firstSheet_lastmonth = book_lastmonth.sheet_by_index(0)
rows_thismonth = firstSheet_thismonth.nrows #how many rows in spreadsheet
rows_lastmonth = firstSheet_lastmonth.nrows

#warn if the table has changed shape (eg more rows)
if (rows_thismonth != rows_lastmonth):
    print "Data has changed shape! Dammit!"

#loop through first spreadsheet and create dictionary for this month
jsa_thismonth = {}



for row in range(rows_thismonth):
    name_cell = firstSheet_thismonth.cell(row, 1) #create a variable to test name_cell and ignore all empty name cell rows
    if name_cell:
           
        jsa_thismonth[row] = {firstSheet_thismonth.cell(row, 1), firstSheet_thismonth.cell(row, 6)}
    else: 
        print "Row: "+row+" is empty. Boo"

#now loop through jsa_thismonth and compare names against cells in firstSheet_lastmonth
#for el in range(len(jsa_thismonth)):
    #print jsa_thismonth[el]

#if placename in jsa_thismonth matches cell in firstSheet_lastmonth AND no cells are empty then create record





import scraperwiki
import lxml.html
import xlrd    
import re
import string
from scraperwiki import scrape

#scrape search page
base_url = 'http://www.ons.gov.uk'
html = scraperwiki.scrape('http://www.ons.gov.uk/ons/datasets-and-tables/index.html?pageSize=50&sortBy=none&sortDirection=none&newquery=jsa01&content-type=Reference+table&content-type=Dataset')


searchtable = lxml.html.fromstring(html)#turn html into lxml object

#identify this month and last month's spreadsheet
thismonth = searchtable.cssselect('table td a')[0]
lastmonth = searchtable.cssselect('table td a')[1]
#extract the relative URL...
thismonth = str(thismonth.xpath('@href')[0])
lastmonth = str(lastmonth.xpath('@href')[0])
#convert into a full URL
thismonth = base_url+thismonth
lastmonth = base_url+lastmonth

#open spreadsheets
book_thismonth = xlrd.open_workbook(file_contents=scrape(thismonth))
book_lastmonth = xlrd.open_workbook(file_contents=scrape(lastmonth))

# You can also access each worksheet by its index
firstSheet_thismonth = book_thismonth.sheet_by_index(0)
firstSheet_lastmonth = book_lastmonth.sheet_by_index(0)
rows_thismonth = firstSheet_thismonth.nrows #how many rows in spreadsheet
rows_lastmonth = firstSheet_lastmonth.nrows

#warn if the table has changed shape (eg more rows)
if (rows_thismonth != rows_lastmonth):
    print "Data has changed shape! Dammit!"

#loop through first spreadsheet and create dictionary for this month
jsa_thismonth = {}



for row in range(rows_thismonth):
    name_cell = firstSheet_thismonth.cell(row, 1) #create a variable to test name_cell and ignore all empty name cell rows
    if name_cell:
           
        jsa_thismonth[row] = {firstSheet_thismonth.cell(row, 1), firstSheet_thismonth.cell(row, 6)}
    else: 
        print "Row: "+row+" is empty. Boo"

#now loop through jsa_thismonth and compare names against cells in firstSheet_lastmonth
#for el in range(len(jsa_thismonth)):
    #print jsa_thismonth[el]

#if placename in jsa_thismonth matches cell in firstSheet_lastmonth AND no cells are empty then create record





