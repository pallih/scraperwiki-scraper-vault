import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

html = scraperwiki.scrape("http://www.seattlemet.com/lists/top-doctors-2012?page=2")
#print html



root = lxml.html.fromstring(html)

for div in root.cssselect("div.content-box div.listing"):
    a = div.cssselect("div.listing")
    name = a[0].cssselect("div.title")[0].text
    addr = a[0].cssselect("div.address")[0].text
    city = a[0].cssselect("div.address")[0].cssselect("br")[0].tail
    #print city
    name = name.strip()

    returned = us.geocode(addr + city)
    if returned != None:
        place, (lat, lng) = returned
    else:
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng) 

    data = {
        'name': name,
     #   'address': addr,
      #  'city': city,
        'lat': lat,
        'long': lng,
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

html = scraperwiki.scrape("http://www.seattlemet.com/lists/top-doctors-2012?page=2")
#print html



root = lxml.html.fromstring(html)

for div in root.cssselect("div.content-box div.listing"):
    a = div.cssselect("div.listing")
    name = a[0].cssselect("div.title")[0].text
    addr = a[0].cssselect("div.address")[0].text
    city = a[0].cssselect("div.address")[0].cssselect("br")[0].tail
    #print city
    name = name.strip()

    returned = us.geocode(addr + city)
    if returned != None:
        place, (lat, lng) = returned
    else:
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng) 

    data = {
        'name': name,
     #   'address': addr,
      #  'city': city,
        'lat': lat,
        'long': lng,
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)