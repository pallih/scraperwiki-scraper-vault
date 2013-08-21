import scraperwiki
import xlrd
import datetime

URL = 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'

#set a variable for the spreadsheet location
XLS = 'https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'

#use the scrape function on that spreadsheet to create a new variable
xlbin = scraperwiki.scrape(XLS)
#use the open_workbook function on that new variable to create another
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (1) to grab the second row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(1)
#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[2]

#put cells from the 15th row into 'keys' variable 
keys = sheet.row_values(14)
keyslist = []
id = 0
for key in keys:
    if isinstance(key, float):
        key = xlrd.xldate_as_tuple(key,0)
        print "date as tuple:",key
        #still cannot convert this using datetime.datetime(key) because generates error saying datetime expects an integer
        #search for 'convert tuple to date python' brings you to solution here: http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/
        key = datetime.datetime(*key[0:6])
        print "date as datetime object:", key
        key = key.strftime("%Y.%m.%d")
        print "date converted using .strftime method:", key
        print "date split by full stop, first index (year) grabbed:", key.split(".")[0]
        key = key.split(".")[0]+"_"+key.split(".")[1]+"_"+key.split(".")[2]
        print "concatenated:", key
        #AFTER ALL THIS, STILL NOT 'SIMPLE TEXT', WHICH BREAKS SCRAPER
        print "converted date?", key
        keyslist.append(str(key))
        print keyslist
    else:
        keyslist.append(str(key))

record = {}
        #loop through a range - from the 18th item (17) to a number generated by using the .nrows method on 'sheet' (to find number of rows in that sheet)
        #put each row number in 'rownumber' as you loop
Name = "no entry"
record['title'] = title[2]
for rownumber in range(17, sheet.nrows):
    print "scraping row ", rownumber
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
    for num in range(1,sheet.ncols):
        record[keyslist[num]] = sheet.row_values(rownumber)[num]
    id = id+1
    record['id'] = id
    print "---", record
    scraperwiki.sqlite.save([keyslist[2], 'id'], record)
import scraperwiki
import xlrd
import datetime

URL = 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'

#set a variable for the spreadsheet location
XLS = 'https://www.wp.dh.gov.uk/transparency/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'

#use the scrape function on that spreadsheet to create a new variable
xlbin = scraperwiki.scrape(XLS)
#use the open_workbook function on that new variable to create another
book = xlrd.open_workbook(file_contents=xlbin)

#use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
sheet = book.sheet_by_index(0)

#use the row_values method and index (1) to grab the second row of 'sheet', and put all cells into the list variable 'title'
title = sheet.row_values(1)
#print the string "Title:", followed by the third item (column) in the variable 'title' 
print "Title:", title[2]

#put cells from the 15th row into 'keys' variable 
keys = sheet.row_values(14)
keyslist = []
id = 0
for key in keys:
    if isinstance(key, float):
        key = xlrd.xldate_as_tuple(key,0)
        print "date as tuple:",key
        #still cannot convert this using datetime.datetime(key) because generates error saying datetime expects an integer
        #search for 'convert tuple to date python' brings you to solution here: http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/
        key = datetime.datetime(*key[0:6])
        print "date as datetime object:", key
        key = key.strftime("%Y.%m.%d")
        print "date converted using .strftime method:", key
        print "date split by full stop, first index (year) grabbed:", key.split(".")[0]
        key = key.split(".")[0]+"_"+key.split(".")[1]+"_"+key.split(".")[2]
        print "concatenated:", key
        #AFTER ALL THIS, STILL NOT 'SIMPLE TEXT', WHICH BREAKS SCRAPER
        print "converted date?", key
        keyslist.append(str(key))
        print keyslist
    else:
        keyslist.append(str(key))

record = {}
        #loop through a range - from the 18th item (17) to a number generated by using the .nrows method on 'sheet' (to find number of rows in that sheet)
        #put each row number in 'rownumber' as you loop
Name = "no entry"
record['title'] = title[2]
for rownumber in range(17, sheet.nrows):
    print "scraping row ", rownumber
        #the next line generates an error if one of the keys is an unconverted date integer (like 41219.0)
        #we worked this out through eliminating that date key with the following adaptation of an earlier line...
        #for num in range(1,sheet.ncols-5)
        #once eliminated, we know we need to convert that date key earlier - see above
    for num in range(1,sheet.ncols):
        record[keyslist[num]] = sheet.row_values(rownumber)[num]
    id = id+1
    record['id'] = id
    print "---", record
    scraperwiki.sqlite.save([keyslist[2], 'id'], record)
