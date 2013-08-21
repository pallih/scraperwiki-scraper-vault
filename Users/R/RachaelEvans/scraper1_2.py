import scraperwiki
import lxml.html
import json
import re
import urllib



print 'Geocoding locations...'
locations = scraperwiki.sqlite.select("* from locations where longitude = '' order by country, city")
for location in locations:
    print 'Geocoding ' + location['location'] + '...'
    raw_json = scraperwiki.scrape('http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=' + urllib.quote(location['location'].encode('utf-8')))
    geo_object = json.loads(raw_json)
    lat = geo_object['results'][0]['geometry']['location']['lat']
    lng = geo_object['results'][0]['geometry']['location']['lng']
    print 'Saving ' + location['city'] + '...'
    scraperwiki.sqlite.execute('update locations set latitude="' + str(lat) + '", longitude="' + str(lng) + '" where location="' + location['location'] + '"')
    scraperwiki.sqlite.commit()

