# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://salaamlove.com/ % i).text
        dom=lxml.html.fromstring (r)
        for name in dom.cssselect('h6'):
            print name


scrape_people()# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://salaamlove.com/ % i).text
        dom=lxml.html.fromstring (r)
        for name in dom.cssselect('h6'):
            print name


scrape_people()