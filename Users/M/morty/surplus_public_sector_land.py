import scraperwiki
import xlrd

url = "http://www.homesandcommunities.co.uk/public/documents/register-of-surplus-public-sector-land-Dec-2010_1.xls"

data = scraperwiki.scrape(url)

book = xlrd.open_workbook(file_contents=data)
sheet = book.sheets()[0]


columns = sheet.row_values(0)

for i in range(2, sheet.nrows):
    row = sheet.row_values(i)
    scraperwiki.sqlite.save(columns, dict(zip(columns, row)))
