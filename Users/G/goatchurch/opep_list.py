import scraperwiki
import xlrd
import re
import urllib2
import datetime


# proper link which currently seems to download a fraction of the file
# https://www.og.decc.gov.uk/environment/arp.htm
url = "https://www.og.decc.gov.uk/environment/OPEP%20spreadsheet.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Plan No.', u'Submission Date', u'Operator', u'Title of Plan', u'Approved']
headings[0] = 'Plan No'

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value


dateerrors = { '-':'', '07 Decmber 2010':datetime.date(2010, 12, 7),
               '04 Decmber 2008':datetime.date(2008, 12, 4), '19 November 20010':datetime.date(2010, 11, 19), 
               40494.0:datetime.date(2010, 11, 11)
             }

for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    data['Plan No'] = int(data['Plan No'])

    data['Submission Date'] = dateerrors.get(data['Submission Date'], data['Submission Date'])
    data['Approved'] = dateerrors.get(data['Approved'], data['Approved'])

    if data['Approved'] == '':
        del data['Approved']
    elif type(data['Approved']) != datetime.date:
        print data
    if type(data['Submission Date']) != datetime.date:
        print data
    scraperwiki.sqlite.save(unique_keys=['Plan No'], data=data)

import scraperwiki
import xlrd
import re
import urllib2
import datetime


# proper link which currently seems to download a fraction of the file
# https://www.og.decc.gov.uk/environment/arp.htm
url = "https://www.og.decc.gov.uk/environment/OPEP%20spreadsheet.xls"

xldata = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=xldata)

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Plan No.', u'Submission Date', u'Operator', u'Title of Plan', u'Approved']
headings[0] = 'Plan No'

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value


dateerrors = { '-':'', '07 Decmber 2010':datetime.date(2010, 12, 7),
               '04 Decmber 2008':datetime.date(2008, 12, 4), '19 November 20010':datetime.date(2010, 11, 19), 
               40494.0:datetime.date(2010, 11, 11)
             }

for irow in range(1, sheet.nrows):
    row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    data['Plan No'] = int(data['Plan No'])

    data['Submission Date'] = dateerrors.get(data['Submission Date'], data['Submission Date'])
    data['Approved'] = dateerrors.get(data['Approved'], data['Approved'])

    if data['Approved'] == '':
        del data['Approved']
    elif type(data['Approved']) != datetime.date:
        print data
    if type(data['Submission Date']) != datetime.date:
        print data
    scraperwiki.sqlite.save(unique_keys=['Plan No'], data=data)

