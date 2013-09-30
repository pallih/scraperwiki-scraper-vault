import scraperwiki
import xlrd

url = 'http://www.education.gov.uk/rsgateway/DB/STA/t000990/nlac-2011.xls'
data = scraperwiki.scrape (url)
book = xlrd.open_workbook (file_contents=data)
sheet = book.sheet_by_index(0)

for i in range(1,sheet.nrows): #skip row 0 (header)
    scraperwiki.sqlite.save (unique_keys=['la_code'], data={'la_code':int(sheet.cell(i,0).value), 'gss_code':sheet.cell(i,1).value, 'la_name':sheet.cell(i,2).value}, table_name='nlac')

import scraperwiki
import xlrd

url = 'http://www.education.gov.uk/rsgateway/DB/STA/t000990/nlac-2011.xls'
data = scraperwiki.scrape (url)
book = xlrd.open_workbook (file_contents=data)
sheet = book.sheet_by_index(0)

for i in range(1,sheet.nrows): #skip row 0 (header)
    scraperwiki.sqlite.save (unique_keys=['la_code'], data={'la_code':int(sheet.cell(i,0).value), 'gss_code':sheet.cell(i,1).value, 'la_name':sheet.cell(i,2).value}, table_name='nlac')

