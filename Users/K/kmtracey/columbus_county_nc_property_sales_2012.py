import scraperwiki
import xlrd
import datetime

xlbin = scraperwiki.scrape('http://www.columbusco.org/GISData/Sales/2012%20Sales%20Report.xls')
#xlbin = scraperwiki.scrape('http://www.columbusco.org/sales.xls')
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)

keys = [u'TWSP', u'PROP', u'GRANTEE', u'GRANTOR', u'TYPE', u'OCCUPANCY', u'ACRES', u'LOTS', u'BOOK', u'PAGE', u'SALE', u'APPRAISAL', u'QSAL', u'RJCT', u'DATE', u'SQFT'] 
#keys = sheet.row_values(0)
#keys[1] = keys[1].replace('#','')
#print keys

for rownumber in range(1, sheet.nrows):
    values = [cell.value for cell in sheet.row(rownumber)]
    data = dict(zip(keys, values))
    scraperwiki.sqlite.save(unique_keys=['PROP', 'DATE'], data=data)
