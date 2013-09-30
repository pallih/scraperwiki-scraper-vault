import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_index(0)

for n, s in enumerate(book.sheets()):
    print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

print sheet.row_values(4)


import datetime
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

print [ cellval(c, book.datemode) for c in sheet.row(4) ]

keys = sheet.row_values(2)
keys[1] = keys[1].replace('.', '')
print keys

for rownumber in range(4, sheet.nrows):
    values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
    data = dict(zip(keys, values))
    data['rownumber'] = rownumber
    del data['']
    if data['DATE'] != None and data['FLEET NO'] != None:
        scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)
import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_index(0)

for n, s in enumerate(book.sheets()):
    print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

print sheet.row_values(4)


import datetime
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

print [ cellval(c, book.datemode) for c in sheet.row(4) ]

keys = sheet.row_values(2)
keys[1] = keys[1].replace('.', '')
print keys

for rownumber in range(4, sheet.nrows):
    values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
    data = dict(zip(keys, values))
    data['rownumber'] = rownumber
    del data['']
    if data['DATE'] != None and data['FLEET NO'] != None:
        scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)
