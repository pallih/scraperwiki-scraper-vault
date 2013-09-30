import scraperwiki

# Blank Python

import scraperwiki

# Blank Python

print "hh"
import lxml.html
import datetime
import dateutil.parser
html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue/mapdetail/2380.html")
root = lxml.html.fromstring(html)
print "hh1"

for el in root.cssselect("tr td"):

    coun = el.text
   
    print coun
    if coun is not None:
            data = {
            'dat' :coun
                   }
            print data
            scraperwiki.sqlite.save(unique_keys=['dat'], data = data)  

print html
import scraperwiki

# Blank Python

import scraperwiki

# Blank Python

print "hh"
import lxml.html
import datetime
import dateutil.parser
html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue/mapdetail/2380.html")
root = lxml.html.fromstring(html)
print "hh1"

for el in root.cssselect("tr td"):

    coun = el.text
   
    print coun
    if coun is not None:
            data = {
            'dat' :coun
                   }
            print data
            scraperwiki.sqlite.save(unique_keys=['dat'], data = data)  

print html
