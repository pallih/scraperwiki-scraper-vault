#copied and pasted, not ready

#%s turns it into a string

import scraperwiki
import requests
import lxml.html

def restaurants():    
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.60by80.com/barcelona/restaurants/' % i).text
        print r

        dom = lxml.html.fromstring(r)
        for name in dom.cssselect('contentheadingsection'):
            print name.text
            d = { 'name': name.text }
            scraperwiki.sqlite.save(['name'], d)
restaurants()
#copied and pasted, not ready

#%s turns it into a string

import scraperwiki
import requests
import lxml.html

def restaurants():    
    for i in range (1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.60by80.com/barcelona/restaurants/' % i).text
        print r

        dom = lxml.html.fromstring(r)
        for name in dom.cssselect('contentheadingsection'):
            print name.text
            d = { 'name': name.text }
            scraperwiki.sqlite.save(['name'], d)
restaurants()
