import scraperwiki           
import lxml.html
import urllib2

html = scraperwiki.scrape("http://data.gov.gh/catalogs?&results=200")
root = lxml.html.fromstring(html)

for el in root.cssselect("table.ds-list a"):
    if el.attrib['href'].endswith('.xls'):
        
        print el.attrib['href']