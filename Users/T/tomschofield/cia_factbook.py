#base_url = "http://www.cia.gov/library/publications/the-world-factbook/geos/xx.html"
base_url = "http://www.tomschofieldart.com"

import scraperwiki           
import lxml.html
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)

#for el in root.cssselect("div.category_data"):           
lis = root.cssselect("body.section-library")
print len(lis)
for el in root.cssselect("body.section-library"):        
    print el
#base_url = "http://www.cia.gov/library/publications/the-world-factbook/geos/xx.html"
base_url = "http://www.tomschofieldart.com"

import scraperwiki           
import lxml.html
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)

#for el in root.cssselect("div.category_data"):           
lis = root.cssselect("body.section-library")
print len(lis)
for el in root.cssselect("body.section-library"):        
    print el
