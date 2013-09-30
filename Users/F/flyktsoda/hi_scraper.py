#%s turns it into a string

import scraperwiki
import requests
import lxml.html

def scrape_people():    
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
        print r
        dom = lxml.html.fromstring(r)
        for name in dom.cssselect('h6'):
            print name.text
            d = { 'name': name.text }
            scraperwiki.sqlite.save(['name'], d)

scrape_people()
#%s turns it into a string

import scraperwiki
import requests
import lxml.html

def scrape_people():    
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
        print r
        dom = lxml.html.fromstring(r)
        for name in dom.cssselect('h6'):
            print name.text
            d = { 'name': name.text }
            scraperwiki.sqlite.save(['name'], d)

scrape_people()
