# Richard McGovern
# Geog 495 Bergmann
# May 8, 2013
#
# DESCRIPTION: Creates a shapefile of public libraries in Seattle by geocoding
#               addresses from http://www.spl.org/locations
#

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("http://www.spl.org/locations")
print html

root = lxml.html.fromstring(html)

headerOuter = root.cssselect("div.header-outer")
print len(headerOuter)

# Create list of library rows. ra and rb are temp vars to avoid clutter.
#ra = headerOuter[0].getnext().getnext().getnext().getnext().getchildren()[0] #tbody
#rb = ra.getchildren()[0].getchildren()[0].getnext().getchildren()[0].getchildren()[0] #tbody
#rows = rb.getchildren()[0].getchildren()[0].getchildren()[0].getnext().getchildren()[0].getchildren()

#for tr in rows:
#    lbrTag = tr.getchildren()[1]
    
#    data = {
#        'libName': lbrTag.getchildren()[0].getchildren()[0].getchildren()[0].text,
#    }
#    scraperwiki.sqlite.save(unique_keys=['libName'],data=data)
#    print data.values()


parList = root.cssselect("p")

# Remove the preliminary paragraphs.
while parList[0].text_content() != "Map of Library Locations":
    parList.pop(0)
parList.pop(0)

for times in range(4):
    parList.pop()

for p in parList:
    print p.text_content()  
    

# Build index identifier
#for p in parList:
    

# Instead:
#parList = [p for p in parList if determine(p)]

# Richard McGovern
# Geog 495 Bergmann
# May 8, 2013
#
# DESCRIPTION: Creates a shapefile of public libraries in Seattle by geocoding
#               addresses from http://www.spl.org/locations
#

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("http://www.spl.org/locations")
print html

root = lxml.html.fromstring(html)

headerOuter = root.cssselect("div.header-outer")
print len(headerOuter)

# Create list of library rows. ra and rb are temp vars to avoid clutter.
#ra = headerOuter[0].getnext().getnext().getnext().getnext().getchildren()[0] #tbody
#rb = ra.getchildren()[0].getchildren()[0].getnext().getchildren()[0].getchildren()[0] #tbody
#rows = rb.getchildren()[0].getchildren()[0].getchildren()[0].getnext().getchildren()[0].getchildren()

#for tr in rows:
#    lbrTag = tr.getchildren()[1]
    
#    data = {
#        'libName': lbrTag.getchildren()[0].getchildren()[0].getchildren()[0].text,
#    }
#    scraperwiki.sqlite.save(unique_keys=['libName'],data=data)
#    print data.values()


parList = root.cssselect("p")

# Remove the preliminary paragraphs.
while parList[0].text_content() != "Map of Library Locations":
    parList.pop(0)
parList.pop(0)

for times in range(4):
    parList.pop()

for p in parList:
    print p.text_content()  
    

# Build index identifier
#for p in parList:
    

# Instead:
#parList = [p for p in parList if determine(p)]

