# Richard McGovern
# Geog 495 Bergmann
# May 10, 2013
#
# DESCRIPTION: Geocodes addresses of sightseeing places in Seattle near Hotelmax
#              based on the addresses provided from this site:
#              http://www.hotelmaxseattle.com/seattle-attractions-sightseeing/
# I faced some fairly serious difficulties with this assignment. I went through 
# about a dozen sites looking for addresses that US Geocoder could geocode and 
# that were also parseable. Some sites had html that was produced dynamically from
# another site, so it was not accessible, other sites had parseable html but had addresses
# that were not geocodable, other sites had geocodable addresses that were so buried in the html
# that I gave up after several hours of meticulous css selection which sadly failed.
# Still other sites yielded all of the above difficulties. There is evidence of my work in other scraper files.
# I eventually lucked out and found this one that seems to work.
# I spent over 10 hours on this assignment.

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("http://www.hotelmaxseattle.com/seattle-attractions-sightseeing/")
print html

root = lxml.html.fromstring(html)

attrSection = root.cssselect("div.attraction_listing")

# Retrieve names, urls, and addresses of each attraction listed.
for div in attrSection:
    linkList = div.cssselect("a")
    brs = div.cssselect("br")
    
    name = linkList[0].text
    url = linkList[1].text
    address = brs[0].tail

    print address
    
    returned = us.geocode(address)
    if returned != None: 
        place, (lat, lng) = returned
    else:

        # Default the geocoding to return that of Pike Place Market if it fails.
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        print "failed to geocode"
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    data = {
        'name': name,
        'url': url,
        'address': address
        'lat': lat
        'long': lng
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
# Richard McGovern
# Geog 495 Bergmann
# May 10, 2013
#
# DESCRIPTION: Geocodes addresses of sightseeing places in Seattle near Hotelmax
#              based on the addresses provided from this site:
#              http://www.hotelmaxseattle.com/seattle-attractions-sightseeing/
# I faced some fairly serious difficulties with this assignment. I went through 
# about a dozen sites looking for addresses that US Geocoder could geocode and 
# that were also parseable. Some sites had html that was produced dynamically from
# another site, so it was not accessible, other sites had parseable html but had addresses
# that were not geocodable, other sites had geocodable addresses that were so buried in the html
# that I gave up after several hours of meticulous css selection which sadly failed.
# Still other sites yielded all of the above difficulties. There is evidence of my work in other scraper files.
# I eventually lucked out and found this one that seems to work.
# I spent over 10 hours on this assignment.

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("http://www.hotelmaxseattle.com/seattle-attractions-sightseeing/")
print html

root = lxml.html.fromstring(html)

attrSection = root.cssselect("div.attraction_listing")

# Retrieve names, urls, and addresses of each attraction listed.
for div in attrSection:
    linkList = div.cssselect("a")
    brs = div.cssselect("br")
    
    name = linkList[0].text
    url = linkList[1].text
    address = brs[0].tail

    print address
    
    returned = us.geocode(address)
    if returned != None: 
        place, (lat, lng) = returned
    else:

        # Default the geocoding to return that of Pike Place Market if it fails.
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        print "failed to geocode"
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    data = {
        'name': name,
        'url': url,
        'address': address
        'lat': lat
        'long': lng
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
