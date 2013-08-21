import scraperwiki
import urlparse
import lxml.html
import xlrd
from datetime import date


url = "http://www.ic.nhs.uk/searchcatalogue?q=title%3A%22national+safety+thermometer+data+quality+report%22&area=&size=10&sort=Most+recent"

def xls_scraper(xlsFile):

    xlbin = scraperwiki.scrape(xlsFile)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(2)
    title = sheet.row_values(3)
    #print "Title:", title[1]

    #put cells from the first row into 'keys' variable 
    keys = sheet.row_values(3)
    record = {}

    for rownumber in range(4, sheet.nrows):
        #print rownumber
        record['Organisation'] = sheet.row_values(rownumber)[1]
        record['DataErrors'] = sheet.row_values(rownumber)[2]
        record['ScrapeDate'] = date.today()
        print "---", record
        scraperwiki.datastore.save(["Organisation"], data=record)

def monthLists(monthPage):
    icPage = 'http://www.ic.nhs.uk/'
    html2 = scraperwiki.scrape(monthPage)
    root2 = lxml.html.fromstring(html2)
    xlsaLink = root2.cssselect("div.resourcelink a")
    #xlsLink = xlsaLink[0].attrib.get('href')
    xlsFile = urlparse.urljoin(icPage, xlsaLink[0].attrib.get('href'))
    xls_scraper(xlsFile)

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
month_link = root.cssselect("li.item.HSCICProducts.first div.title a")
monthPage = month_link[0].attrib.get('href')
monthLists(monthPage)







