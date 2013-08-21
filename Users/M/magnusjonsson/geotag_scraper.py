###############################################################################
# Examples of geocoding data with different free services
###############################################################################

import scraperwiki
import urllib
import urllib2
import simplejson

# street_address is the address we are trying to encode.
street_address = 'brasil'


# Google maps
# - Works world wide (at least in the countries listed here: http://gmaps-samples.googlecode.com/svn/trunk/mapcoverage_filtered.html)
# - limited to 2,500 requests in a 24 hour period (more details here: http://code.google.com/apis/maps/faq.html#geocoder_limit)
geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(street_address)+'&sensor=false&output=json'
print geocode_url
georeq = urllib2.Request(geocode_url)
geo_response = urllib2.urlopen(georeq)
geocode = simplejson.loads(geo_response.read())
print geocode
if geocode['status'] != 'ZERO_RESULTS':
    data_lat = geocode['results'][0]['geometry']['location']['lat']
    data_lng = geocode['results'][0]['geometry']['location']['lng']

print data_lat 
print data_lng

# ESRI Locator service
# - Currently USA addresses only
# - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
#geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+urllib.quote_plus(street_address)+'&outFields=&outSR=&f=json'
#print geocode_url
#georeq = urllib2.Request(geocode_url)
#geo_response = urllib2.urlopen(georeq)
#geocode = simplejson.loads(geo_response.read())
#print geocode
#if len(geocode['candidates']):
#    data_lat = geocode['candidates'][0]['location']['y']
#    data_lng = geocode['candidates'][0]['location']['x']

#print data_lat 
#print data_lng

# ESRI Locator service- for EU
# - EU addresses only
# - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
#geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Address_EU/GeocodeServer/findAddressCandidates?Single+Line+Input='+urllib.quote_plus(street_address)+'&outFields=&outSR=&f=json'
#print geocode_url
#georeq = urllib2.Request(geocode_url)
#geo_response = urllib2.urlopen(georeq)
#geocode = simplejson.loads(geo_response.read())
#print geocode
#if len(geocode['candidates']):
   # data_lat = geocode['candidates'][0]['location']['y']
   # data_lng = geocode['candidates'][0]['location']['x']

#print data_lat 
#print data_lng
