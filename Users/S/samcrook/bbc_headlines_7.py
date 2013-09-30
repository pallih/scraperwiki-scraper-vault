import scraperwiki
import BeautifulSoup
import urllib2, datetime, sys
from urllib2 import HTTPError
from scraperwiki import datastore

#scrape page
for id in range(10100,84516):
    url = 'http://www.doughty-engineering.co.uk/cgi-bin/trolleyed_public.cgi?action=showprod_T%s' %(id,)
    
    try:
        request = urllib2.urlopen(url)
    except HTTPError,e :
        if (e.code ==404):
            print 'Not Found: %s' %(url)
        continue
    
    html = request.read()


    page = BeautifulSoup.BeautifulSoup(html)

    try:
        description = page.find("td", { "class" : "product-description" })

        date = datetime.datetime.now()
    
        datastore.save(['id'],{'id':id, 'description':description,},date)
    except:
        print "Unexpected error:", sys.exc_info()[0]


import scraperwiki
import BeautifulSoup
import urllib2, datetime, sys
from urllib2 import HTTPError
from scraperwiki import datastore

#scrape page
for id in range(10100,84516):
    url = 'http://www.doughty-engineering.co.uk/cgi-bin/trolleyed_public.cgi?action=showprod_T%s' %(id,)
    
    try:
        request = urllib2.urlopen(url)
    except HTTPError,e :
        if (e.code ==404):
            print 'Not Found: %s' %(url)
        continue
    
    html = request.read()


    page = BeautifulSoup.BeautifulSoup(html)

    try:
        description = page.find("td", { "class" : "product-description" })

        date = datetime.datetime.now()
    
        datastore.save(['id'],{'id':id, 'description':description,},date)
    except:
        print "Unexpected error:", sys.exc_info()[0]


