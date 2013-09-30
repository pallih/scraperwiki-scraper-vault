# Blank Python
import scraperwiki
import urllib
from geopy import geocoders

print help(geocoders)

baseurl = "http://maps.googleapis.com/maps/api/geocode/json?address="
sourcescraper = 'missing_persons_usa'
scraperwiki.sqlite.attach(sourcescraper)
select = scraperwiki.sqlite.select("* from missing_persons_usa")
for s in select:
    location = s['location']
    #geturl = baseurl + urllib.quote(location.encode('utf-8')) +'&sensor=false'
    #json = scraperwiki.scrape(geturl)
    #print json
    g = geocoders.GeoNames()
    place, (lat, lng) = g.geocode(location,exactly_one=True)  
    print "%s: %.5f, %.5f" % (place, lat, lng)   





# Blank Python
import scraperwiki
import urllib
from geopy import geocoders

print help(geocoders)

baseurl = "http://maps.googleapis.com/maps/api/geocode/json?address="
sourcescraper = 'missing_persons_usa'
scraperwiki.sqlite.attach(sourcescraper)
select = scraperwiki.sqlite.select("* from missing_persons_usa")
for s in select:
    location = s['location']
    #geturl = baseurl + urllib.quote(location.encode('utf-8')) +'&sensor=false'
    #json = scraperwiki.scrape(geturl)
    #print json
    g = geocoders.GeoNames()
    place, (lat, lng) = g.geocode(location,exactly_one=True)  
    print "%s: %.5f, %.5f" % (place, lat, lng)   





