# Pinball Machines in Seattle!

import scraperwiki
import lxml.html
import lxml.etree
import urllib
import geopy
from geopy import geocoders   
import string

us = geocoders.GeocoderDotUS()  
gn = geocoders.GeoNames()   

html = scraperwiki.scrape("http://list.skill-shot.com/")
root = lxml.html.fromstring(html)

print len(root.cssselect("div [class='location']"))
locations = root.cssselect("div [class='location']")

for pinball in root.cssselect("div [class='location']"):
    venue = pinball.cssselect("a")[0].text
    address = pinball.cssselect("h4")[0].text
    table = pinball.cssselect("li")[0].text

    tables = []
    for tables in pinball.cssselect("li"):
        tables.append(table.rstrip().split(','))

    returned = us.geocode(address + ", Seattle, WA")
    if returned != None: 
        place, (lat, lng) = returned
        print place
    else:
        place, (lat, lng) = us.geocode("6360 Wing Point Road NE, Bainbridge Island, WA, 98110")
        place = "GEOCODE FAIL" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    print venue
    print address
    print table

    data = {
        'venue': venue,
        'address': address,
        'table' : table,
        'lat': lat,         
        'long': lng,         
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['venue'],data=data)


# SCRATCH:


#    for table in pinball.cssselect("li"):
#        print table.text
#        tables = ", "
#        tables.join(table.text)


#    for iter in range(len(pinball.cssselect("li"))):
#        print len(pinball.cssselect("li"))[iter].text
#    multitable = 0
#    table = pinball.cssselect("li")[multitable].text
#    while table != None:
#        multitable += 1

# Pinball Machines in Seattle!

import scraperwiki
import lxml.html
import lxml.etree
import urllib
import geopy
from geopy import geocoders   
import string

us = geocoders.GeocoderDotUS()  
gn = geocoders.GeoNames()   

html = scraperwiki.scrape("http://list.skill-shot.com/")
root = lxml.html.fromstring(html)

print len(root.cssselect("div [class='location']"))
locations = root.cssselect("div [class='location']")

for pinball in root.cssselect("div [class='location']"):
    venue = pinball.cssselect("a")[0].text
    address = pinball.cssselect("h4")[0].text
    table = pinball.cssselect("li")[0].text

    tables = []
    for tables in pinball.cssselect("li"):
        tables.append(table.rstrip().split(','))

    returned = us.geocode(address + ", Seattle, WA")
    if returned != None: 
        place, (lat, lng) = returned
        print place
    else:
        place, (lat, lng) = us.geocode("6360 Wing Point Road NE, Bainbridge Island, WA, 98110")
        place = "GEOCODE FAIL" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    print venue
    print address
    print table

    data = {
        'venue': venue,
        'address': address,
        'table' : table,
        'lat': lat,         
        'long': lng,         
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['venue'],data=data)


# SCRATCH:


#    for table in pinball.cssselect("li"):
#        print table.text
#        tables = ", "
#        tables.join(table.text)


#    for iter in range(len(pinball.cssselect("li"))):
#        print len(pinball.cssselect("li"))[iter].text
#    multitable = 0
#    table = pinball.cssselect("li")[multitable].text
#    while table != None:
#        multitable += 1

