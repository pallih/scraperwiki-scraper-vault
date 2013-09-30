import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string


us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  



html = scraperwiki.scrape("http://www.seattlefoodtruck.com/index.php/by-day/monday/")
print html

root = lxml.html.fromstring(html)

for tr in root.cssselect("div.entry-content tr"):

    tds = tr.cssselect("td")

    foodtruckurl = tds[0].cssselect("h5")[0].cssselect("a")[0].attrib['href']
    foodtruckname = tds[0].cssselect("h5")[0].cssselect("a")[0].text
    
    address_and_time = tds[1].cssselect('br')[0].tail

    address = ",".join(address_and_time.split(",")[0:-1]) 
    hours = address_and_time.split(",")[-1]

    print address
    address_2 = filter(lambda c: c in string.digits + ',' + '.' + ' ' + "#" + string.letters, address)   
    print address_2

    returned = us.geocode(address_2 + citystate)
    if returned != None: 
        place, (lat, lng) = returned
    else:
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    data = {
        'name': foodtruckname,
        'url': foodtruckurl,
        'hours': hours,
        'lat': lat,
        'long': lng,
        'address': address,
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



html = scraperwiki.scrape("http://www.seattlefoodtruck.com/index.php/by-day/monday/")
print html

root = lxml.html.fromstring(html)

for tr in root.cssselect("div.entry-content tr"):

    tds = tr.cssselect("td")

    foodtruckurl = tds[0].cssselect("h5")[0].cssselect("a")[0].attrib['href']
    foodtruckname = tds[0].cssselect("h5")[0].cssselect("a")[0].text
    
    address_and_time = tds[1].cssselect('br')[0].tail

    address = ",".join(address_and_time.split(",")[0:-1]) 
    hours = address_and_time.split(",")[-1]

    print address
    address_2 = filter(lambda c: c in string.digits + ',' + '.' + ' ' + "#" + string.letters, address)   
    print address_2

    returned = us.geocode(address_2 + citystate)
    if returned != None: 
        place, (lat, lng) = returned
    else:
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
    data = {
        'name': foodtruckname,
        'url': foodtruckurl,
        'hours': hours,
        'lat': lat,
        'long': lng,
        'address': address,
        'geocoder result': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
