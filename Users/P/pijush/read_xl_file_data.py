import lxml.html
import datetime
import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)
#sheet = book.sheet_by_name('LAUDERDALE AVE')
#print 'enumerat',len(enumerate(book.sheets())
key={}
i=0
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value
def Mess(num,num2):
    print num+num2

#print [ cellval(c, book.datemode) for c in sheet.row(4) ]
#Mess(9,6)

for n, s in enumerate(book.sheets()):
    #print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    #print sheet.row_values(4)
    #print sheet.cell(4,5)
    #print sheet.col_values(5)
    keys = sheet.row_values(2)
    #print keys[1]
    for k in keys:
        key[i]=k.replace('.','')
        i+=1 
    #keys = keys.replace('.', '')
   # print 'key is', key
    #print keys[1]
for rownumber in range(4, sheet.nrows):
    # create dictionary of the row values
    values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
    data = dict(zip(keys, values))
    data['rownumber'] = rownumber

    # remove the empty column (which has a blank heading)
    del data['']

    # only save if it is a full row (rather than a blank line or a note)
#if data['DATE'] != None and data['FLEET NO'] != None:
  # scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)




import lxml.html
import datetime
import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)
#sheet = book.sheet_by_name('LAUDERDALE AVE')
#print 'enumerat',len(enumerate(book.sheets())
key={}
i=0
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value
def Mess(num,num2):
    print num+num2

#print [ cellval(c, book.datemode) for c in sheet.row(4) ]
#Mess(9,6)

for n, s in enumerate(book.sheets()):
    #print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    #print sheet.row_values(4)
    #print sheet.cell(4,5)
    #print sheet.col_values(5)
    keys = sheet.row_values(2)
    #print keys[1]
    for k in keys:
        key[i]=k.replace('.','')
        i+=1 
    #keys = keys.replace('.', '')
   # print 'key is', key
    #print keys[1]
for rownumber in range(4, sheet.nrows):
    # create dictionary of the row values
    values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
    data = dict(zip(keys, values))
    data['rownumber'] = rownumber

    # remove the empty column (which has a blank heading)
    del data['']

    # only save if it is a full row (rather than a blank line or a note)
#if data['DATE'] != None and data['FLEET NO'] != None:
  # scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)




