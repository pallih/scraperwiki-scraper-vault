###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib2

places = ['Aduna','Andoain','Astigarraga','Ataun','Azpeitia','Donostia','Hernani','Ikaztegieta','Irun','Renteria','Tolosa','Urnieta','Usurbil','Zerain']


base_url = 'http://www.sagardotegi.eu/poblaciones/'

#'VideoHive After Effects set 72'

for p in places:
    html = scraperwiki.scrape(base_url+p.lower())
    root = lxml.html.fromstring(html)
    links = root.cssselect("div.lista_sidrerias_valor a")

    print links.count()
    
    for link in links:

        print links[0].text
    #print lxml.html.tostring(links[0])

