import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string


us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

html = scraperwiki.scrape("http://www.chefseattle.com/restaurants/best-of-seattle/")
print html 

root = lxml.html.fromstring(html)

for div in root.cssselect("div.rv_list div.row"):

    a = div.cssselect("div.row")
    rname = a[0].cssselect("div.c2")[0].cssselect("div")[0].cssselect("a")[0].text
    address =  a[0].cssselect("div.c2")[0].cssselect("div.addr")[0].text
    citystate = a[0].cssselect("div.c2")[0].cssselect("div.addr")[0].cssselect("br")[0].tail

    returned = us.geocode(address + citystate)
    if returned != None:
        place, (lat, lng) = returned
    print "%s: %.5f, %.5f" % (place, lat, lng) 

    data = {
        'name': rname,
        'address': address,
        'city': citystate,
        'lat': lat,
        'long': lng,
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string


us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

html = scraperwiki.scrape("http://www.chefseattle.com/restaurants/best-of-seattle/")
print html 

root = lxml.html.fromstring(html)

for div in root.cssselect("div.rv_list div.row"):

    a = div.cssselect("div.row")
    rname = a[0].cssselect("div.c2")[0].cssselect("div")[0].cssselect("a")[0].text
    address =  a[0].cssselect("div.c2")[0].cssselect("div.addr")[0].text
    citystate = a[0].cssselect("div.c2")[0].cssselect("div.addr")[0].cssselect("br")[0].tail

    returned = us.geocode(address + citystate)
    if returned != None:
        place, (lat, lng) = returned
    print "%s: %.5f, %.5f" % (place, lat, lng) 

    data = {
        'name': rname,
        'address': address,
        'city': citystate,
        'lat': lat,
        'long': lng,
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
