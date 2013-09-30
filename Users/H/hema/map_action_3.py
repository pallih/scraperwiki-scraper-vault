import scraperwiki

# Blank Python

print "hh"
import lxml.html
import datetime
import dateutil.parser
html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue.html")
root = lxml.html.fromstring(html)
print "hh1"

for el in root.cssselect("h2 a"):
#for el in root.cssselect("h2 a"):
    coun = el.text
    print coun
    if coun is not None:
            data = {
            'country' :coun,
                   }
            print data
            scraperwiki.sqlite.save(unique_keys=['country'], data = data)  

print htmlimport scraperwiki

# Blank Python

print "hh"
import lxml.html
import datetime
import dateutil.parser
html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue.html")
root = lxml.html.fromstring(html)
print "hh1"

for el in root.cssselect("h2 a"):
#for el in root.cssselect("h2 a"):
    coun = el.text
    print coun
    if coun is not None:
            data = {
            'country' :coun,
                   }
            print data
            scraperwiki.sqlite.save(unique_keys=['country'], data = data)  

print html