import scraperwiki
import xlrd

xlbin = scraperwiki.scrape("http://www.education.gov.uk/rsgateway/DB/SFR/s001030/sfr25-2011ntv2.xls")
book = xlrd.open_workbook(file_contents=xlbin)

print "Workbook has %s sheet(s)" % book.nsheets

for sheet in book.sheets():
   print "Sheet called %s has %s rows and %s columns" % (sheet.name,sheet.nrows,sheet.ncols)


print sheet.row_values(4)

import datetime
def cellval(cell, datemode):
   if cell.ctype == xlrd.XL_CELL_DATE:
       datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
       if datetuple[3:] == (0, 0, 0):
           return datetime.date(datetuple[0], datetuple[1],
datetuple[2])
       return datetime.date(datetuple[0], datetuple[1], datetuple[2],
datetuple[3], datetuple[4], datetuple[5])
   if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
   if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
   return cell.value

import scraperwiki
keys = sheet.row_values(2)
keys=[key.replace('.', '').replace(':','').replace('(','').replace(')','') for key in keys] #More replacements (Tom)
print keys

for rownumber in range(4, sheet.nrows):
   # create dictionary of the row values
   values = [ cellval(c, book.datemode) for c in
sheet.row(rownumber) ]
   data = dict(zip(keys, values))
   data['rownumber'] = rownumber
   print data

   # remove the empty column (which has a blank heading)
   del data['']

   # only save if it is a full row (rather than a blank line or a note)
   if 'data' not in data.keys() and 'OVERALL ABSENCE' not in data.keys(): #This is what you meant (Tom)
       scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)