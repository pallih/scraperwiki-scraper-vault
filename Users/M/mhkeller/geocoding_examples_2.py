###############################################################################
# Examples of geocoding data with different free services
###############################################################################

import scraperwiki
import urllib
import urllib2
import simplejson

# street_address is the address we are trying to encode.
street_address = '5514 ARNOLD AVENUE, new york new york'

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

print 'Lat:', data_lat, '  Lon:', data_lng


###############################################################################
# Examples of geocoding data with different free services
###############################################################################

import scraperwiki
import urllib
import urllib2
import simplejson

# street_address is the address we are trying to encode.
street_address = '5514 ARNOLD AVENUE, new york new york'

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

print 'Lat:', data_lat, '  Lon:', data_lng


