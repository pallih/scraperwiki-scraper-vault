import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# Data is in Excel sheet.  Holding page is
# https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/basic_onshore_info.htm

url = "https://www.og.decc.gov.uk/upstream/licensing/onshore_10th/landwells.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
assert headings == ['NUMBER', 'WELLSORTABLE', 'NAME', 'OPERATOR', 'LICENCE', 
                    'RELEASED', 'East', 'North', 'LongitudeDegree', 'LongitudeMinute', 'LongitudeSecond', 
                    'LatitudeDegree', 'LatitudeMinute', 'LatitudeSecond', 
                    'DEV', 'COUNTY', 'SPUD', 'COMPLETED', 'INTENT'], headings

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

ldata = [ ]
for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    #print irow, data

    latsecond = data.pop(u'LatitudeSecond')
    if latsecond[-1] == "N" or latsecond[-1] == "n":
        latsecond = latsecond[:-1]
    data["lat"] = data.pop(u'LatitudeDegree') + data.pop(u'LatitudeMinute')/60 + float(latsecond)/3600

    lngsecond = data.pop(u'LongitudeSecond')
    data["lng"] = data.pop(u'LongitudeDegree') + data.pop(u'LongitudeMinute')/60 + float(lngsecond[:-1])/3600
    if lngsecond[-1] == "W":
        data["lng"] = -data["lng"]
    ldata.append(data)
scraperwiki.sqlite.save(unique_keys=["NAME", "WELLSORTABLE", "NUMBER"], data=ldata)

