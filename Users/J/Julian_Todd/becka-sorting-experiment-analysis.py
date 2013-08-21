# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
from scraperwiki import scrape

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=scrape(url))
sheet = book.sheet_by_index(0)
print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value)
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects
#print subjects

for subjectnumber, groups in subjects.iteritems():
    objectlist = [ ]
    for objects in groups.values():
        objectlist.extend(objects)
    if len(objectlist) != len(set(objectlist)):
        print "There is a double count in subject", subjectnumber
    if len(objectlist) != 150:
        print "Subject %d has %d items" % (subjectnumber, len(objectlist))



# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
from scraperwiki import scrape

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=scrape(url))
sheet = book.sheet_by_index(0)
print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value)
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects
#print subjects

for subjectnumber, groups in subjects.iteritems():
    objectlist = [ ]
    for objects in groups.values():
        objectlist.extend(objects)
    if len(objectlist) != len(set(objectlist)):
        print "There is a double count in subject", subjectnumber
    if len(objectlist) != 150:
        print "Subject %d has %d items" % (subjectnumber, len(objectlist))



# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
from scraperwiki import scrape

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=scrape(url))
sheet = book.sheet_by_index(0)
print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value)
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects
#print subjects

for subjectnumber, groups in subjects.iteritems():
    objectlist = [ ]
    for objects in groups.values():
        objectlist.extend(objects)
    if len(objectlist) != len(set(objectlist)):
        print "There is a double count in subject", subjectnumber
    if len(objectlist) != 150:
        print "Subject %d has %d items" % (subjectnumber, len(objectlist))



# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
from scraperwiki import scrape

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=scrape(url))
sheet = book.sheet_by_index(0)
print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value)
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects
#print subjects

for subjectnumber, groups in subjects.iteritems():
    objectlist = [ ]
    for objects in groups.values():
        objectlist.extend(objects)
    if len(objectlist) != len(set(objectlist)):
        print "There is a double count in subject", subjectnumber
    if len(objectlist) != 150:
        print "Subject %d has %d items" % (subjectnumber, len(objectlist))



# xlrd is a library for examining and extracting data from Excel spreadsheets
# Documentation is available here: 
# http://www.lexicon.net/sjmachin/xlrd.html
# Perhaps the best way to learn it is to read the source (Luke!) at:
# http://python-xlrd.sourcearchive.com/documentation/0.6.1/files.html
import xlrd    

import re
from scraperwiki import scrape

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=scrape(url))
sheet = book.sheet_by_index(0)
print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value)
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects
#print subjects

for subjectnumber, groups in subjects.iteritems():
    objectlist = [ ]
    for objects in groups.values():
        objectlist.extend(objects)
    if len(objectlist) != len(set(objectlist)):
        print "There is a double count in subject", subjectnumber
    if len(objectlist) != 150:
        print "Subject %d has %d items" % (subjectnumber, len(objectlist))



