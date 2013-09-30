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
scraperwiki.sqlite.attach("geocoder")
properties = scraperwiki.sqlite.select("address, price, date, lat, lon from [geocoder].swdata where lat = '[]'")
#GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'
GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&%s'

i = 0

for prop in properties:
    address = prop['address']
    price = prop['price']
    sdate = prop['date']
    lat = prop['lat']
    lon = prop['lon']
    if address != "Address":
        if i < 1:
            i = i +1
            url = GEOCODE_URL % urlencode({'address': address})      
            try:
                results_json = simplejson.loads(scraperwiki.scrape(url))  
                print results_json 
                if results_json['status'] != 'ZERO_RESULTS':
                    print "A-OK"
                    #data_lat = results_json['results'][0]['geometry']['location']['lat']
                    #data_lng = results_json['results'][0]['geometry']['location']['lng']
                    #print data_lat
                    #print data_lng
            except:
                print "error"

# street_address is the address we are trying to encode.
#street_address = '85 2nd St San Francisco CA 94105'

# Google maps
# - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
# - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
#geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(street_address)+'&sensor=false&output=json'
#print geocode_url
#georeq = urllib2.Request(geocode_url)
#geo_response = urllib2.urlopen(georeq)
#geocode = simplejson.loads(geo_response.read())
#print geocode
#if geocode['status'] != 'ZERO_RESULTS':
#    data_lat = geocode['results'][0]['geometry']['location']['lat']
#    data_lng = geocode['results'][0]['geometry']['location']['lng']

#print data_lat 
#print data_lngimport scraperwiki
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
scraperwiki.sqlite.attach("geocoder")
properties = scraperwiki.sqlite.select("address, price, date, lat, lon from [geocoder].swdata where lat = '[]'")
#GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'
GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&%s'

i = 0

for prop in properties:
    address = prop['address']
    price = prop['price']
    sdate = prop['date']
    lat = prop['lat']
    lon = prop['lon']
    if address != "Address":
        if i < 1:
            i = i +1
            url = GEOCODE_URL % urlencode({'address': address})      
            try:
                results_json = simplejson.loads(scraperwiki.scrape(url))  
                print results_json 
                if results_json['status'] != 'ZERO_RESULTS':
                    print "A-OK"
                    #data_lat = results_json['results'][0]['geometry']['location']['lat']
                    #data_lng = results_json['results'][0]['geometry']['location']['lng']
                    #print data_lat
                    #print data_lng
            except:
                print "error"

# street_address is the address we are trying to encode.
#street_address = '85 2nd St San Francisco CA 94105'

# Google maps
# - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
# - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
#geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(street_address)+'&sensor=false&output=json'
#print geocode_url
#georeq = urllib2.Request(geocode_url)
#geo_response = urllib2.urlopen(georeq)
#geocode = simplejson.loads(geo_response.read())
#print geocode
#if geocode['status'] != 'ZERO_RESULTS':
#    data_lat = geocode['results'][0]['geometry']['location']['lat']
#    data_lng = geocode['results'][0]['geometry']['location']['lng']

#print data_lat 
#print data_lng