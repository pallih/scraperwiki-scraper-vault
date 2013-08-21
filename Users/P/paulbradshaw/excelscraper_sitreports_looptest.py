#Sandbox to solve two problems: 
#1. identify the number of columns and use that to specify how many to grab
#2. using a loop to write our code for us, rather than having to store data line by line
#3. using column headings as our keys
#4. two headings are dates, which need converting to strings otherwise they kill the scraper

#import scraperwiki library 
import scraperwiki
import datetime
import time

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

#set a variable for the spreadsheet location
XLS = 'https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'

#use the scrape function on that spreadsheet to create a new variable 'xlbin'
xlbin = scraperwiki.scrape(XLS)
#use the open_workbook function on that new variable to create another, 'book'
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (1) to grab the second row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(1)
#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[2]

#put cells from the 15th row into 'keys' variable 
keys1 = sheet.row_values(14)
keys = []
for key in keys1:
#NEED TO CONVERT FROM DATE INTEGER TO ACTUAL DATE - MORE ON DATE INTEGER AT http://www.cpearson.com/excel/datetime.htm
#"Excel stores dates and times as a number representing the number of days since 1900-Jan-0, plus a fractional portion of a 24 hour day:   ddddd.tttttt"
#Loads on Python and dates here: http://www.tutorialspoint.com/python/python_date_time.htm
#Part of xlrd library does this: http://www.lexicon.net/sjmachin/xlrd.html#xlrd.xldate_as_tuple-function
#But that generates an error when it's used on non-dates, so we need an if test to check if it's a float
#taken from:http://stackoverflow.com/questions/4541155/check-if-a-number-is-int-or-float
    if isinstance(key, float):
        key = xlrd.xldate_as_tuple(key,0)
        print "date as tuple:",key
        #still cannot convert this using datetime.datetime(key) because generates error saying datetime expects an integer
        #search for 'convert tuple to date python' brings you to solution here: http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/
        key = datetime.datetime(*key[0:6])
        print "date as datetime object:", key
#        print 
        key = key.strftime("%Y.%m.%d")
        print "date converted using .strftime method:", key
#        key = key.split(".")[0]
        print "date split by full stop, first index (year) grabbed:", key.split(".")[0]
        key = key.split(".")[0]+"_"+key.split(".")[1]+"_"+key.split(".")[2]
        print "concatenated:", key
        #AFTER ALL THIS, STILL NOT 'SIMPLE TEXT', WHICH BREAKS SCRAPER
    print "converted date?", key
    keys.append(str(key))
    
record = {}
print "keys", keys

#print how many columns the sheet has
print "sheet.ncols: ", sheet.ncols
idno = 0
for rownumber in range(17, sheet.nrows):
    print "scraping row ", rownumber
    Name = "no entry"
    for num in range(1,sheet.ncols):
        print "column number:", num
        record['title'] = title[2]
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
        record[keys[num]] = sheet.row_values(rownumber)[num]
    idno = idno + 1
    record['id'] = str(idno)
    print "---", record
    scraperwiki.sqlite.save([keys[2]], record)
    

#spreadsheet found at 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'#Sandbox to solve two problems: 
#1. identify the number of columns and use that to specify how many to grab
#2. using a loop to write our code for us, rather than having to store data line by line
#3. using column headings as our keys
#4. two headings are dates, which need converting to strings otherwise they kill the scraper

#import scraperwiki library 
import scraperwiki
import datetime
import time

#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

#set a variable for the spreadsheet location
XLS = 'https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'

#use the scrape function on that spreadsheet to create a new variable 'xlbin'
xlbin = scraperwiki.scrape(XLS)
#use the open_workbook function on that new variable to create another, 'book'
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (1) to grab the second row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(1)
#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[2]

#put cells from the 15th row into 'keys' variable 
keys1 = sheet.row_values(14)
keys = []
for key in keys1:
#NEED TO CONVERT FROM DATE INTEGER TO ACTUAL DATE - MORE ON DATE INTEGER AT http://www.cpearson.com/excel/datetime.htm
#"Excel stores dates and times as a number representing the number of days since 1900-Jan-0, plus a fractional portion of a 24 hour day:   ddddd.tttttt"
#Loads on Python and dates here: http://www.tutorialspoint.com/python/python_date_time.htm
#Part of xlrd library does this: http://www.lexicon.net/sjmachin/xlrd.html#xlrd.xldate_as_tuple-function
#But that generates an error when it's used on non-dates, so we need an if test to check if it's a float
#taken from:http://stackoverflow.com/questions/4541155/check-if-a-number-is-int-or-float
    if isinstance(key, float):
        key = xlrd.xldate_as_tuple(key,0)
        print "date as tuple:",key
        #still cannot convert this using datetime.datetime(key) because generates error saying datetime expects an integer
        #search for 'convert tuple to date python' brings you to solution here: http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/
        key = datetime.datetime(*key[0:6])
        print "date as datetime object:", key
#        print 
        key = key.strftime("%Y.%m.%d")
        print "date converted using .strftime method:", key
#        key = key.split(".")[0]
        print "date split by full stop, first index (year) grabbed:", key.split(".")[0]
        key = key.split(".")[0]+"_"+key.split(".")[1]+"_"+key.split(".")[2]
        print "concatenated:", key
        #AFTER ALL THIS, STILL NOT 'SIMPLE TEXT', WHICH BREAKS SCRAPER
    print "converted date?", key
    keys.append(str(key))
    
record = {}
print "keys", keys

#print how many columns the sheet has
print "sheet.ncols: ", sheet.ncols
idno = 0
for rownumber in range(17, sheet.nrows):
    print "scraping row ", rownumber
    Name = "no entry"
    for num in range(1,sheet.ncols):
        print "column number:", num
        record['title'] = title[2]
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
        record[keys[num]] = sheet.row_values(rownumber)[num]
    idno = idno + 1
    record['id'] = str(idno)
    print "---", record
    scraperwiki.sqlite.save([keys[2]], record)
    

#spreadsheet found at 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'