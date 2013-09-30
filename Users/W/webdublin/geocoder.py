import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter
from urllib import urlencode
from json import loads, dumps



# Getting output of property scraper
scraperwiki.sqlite.attach("property")
properties = scraperwiki.sqlite.select("address, price, date from [property].swdata")
GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'
#GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=true&%s'

for prop in properties:
    address = prop['address']
    price = prop['price']
    sdate = prop['date']
    if address != "Address":
        #url = GEOCODE_URL % urlencode({'address': address})      
        url = GEOCODE_URL % urlencode({'q': address})      
        try:
            results_json = simplejson.loads(scraperwiki.scrape(url))  
            lat = [(match[u'lat']) for match in results_json]
            lon = [(match[u'lon']) for match in results_json]
            scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address.encode('utf_8'), "price":price, "date":sdate, "lat":lat, "lon":lon})              
        except:
            print "error"
import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import datetime
import operator
from operator import itemgetter, attrgetter
from urllib import urlencode
from json import loads, dumps



# Getting output of property scraper
scraperwiki.sqlite.attach("property")
properties = scraperwiki.sqlite.select("address, price, date from [property].swdata")
GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'
#GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=true&%s'

for prop in properties:
    address = prop['address']
    price = prop['price']
    sdate = prop['date']
    if address != "Address":
        #url = GEOCODE_URL % urlencode({'address': address})      
        url = GEOCODE_URL % urlencode({'q': address})      
        try:
            results_json = simplejson.loads(scraperwiki.scrape(url))  
            lat = [(match[u'lat']) for match in results_json]
            lon = [(match[u'lon']) for match in results_json]
            scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address.encode('utf_8'), "price":price, "date":sdate, "lat":lat, "lon":lon})              
        except:
            print "error"
