import scraperwiki
html = scraperwiki.scrape("http://www.urbanspoon.com/s/1?q=capitol+hill+coffee")

import geopy
from geopy import geocoders

import lxml.html
root = lxml.html.fromstring(html)

oid = 0
for details in root.cssselect("div.restaurants li.restaurant"):
    name = details.cssselect("a.resto_name")[0].text.strip()
    address = details.cssselect("span.address")[0].text.strip()
    price = details.cssselect("span.price")[0].text.strip()
    returned = geocoders.GeocoderDotUS().geocode(address + ", Seattle, WA")
    if returned != None: 
        place, (lat, lng) = returned
    else:
        (lat, lng) = ("0", "0")
    print lat
    print lng

    data = {
        'oid': oid,
        'name': name,
        'address': address,
        'price': price,
        'lat': lat,
        'long': lng,
        'address': address,
    }
    oid = oid + 1
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
    
    









    
import scraperwiki
html = scraperwiki.scrape("http://www.urbanspoon.com/s/1?q=capitol+hill+coffee")

import geopy
from geopy import geocoders

import lxml.html
root = lxml.html.fromstring(html)

oid = 0
for details in root.cssselect("div.restaurants li.restaurant"):
    name = details.cssselect("a.resto_name")[0].text.strip()
    address = details.cssselect("span.address")[0].text.strip()
    price = details.cssselect("span.price")[0].text.strip()
    returned = geocoders.GeocoderDotUS().geocode(address + ", Seattle, WA")
    if returned != None: 
        place, (lat, lng) = returned
    else:
        (lat, lng) = ("0", "0")
    print lat
    print lng

    data = {
        'oid': oid,
        'name': name,
        'address': address,
        'price': price,
        'lat': lat,
        'long': lng,
        'address': address,
    }
    oid = oid + 1
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
    
    









    
