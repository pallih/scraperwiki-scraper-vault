import scraperwiki
import urllib
import lxml.html
import json
import re

#http://en.wikipedia.org/wiki/Political_divisions_of_the_United_States
index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=Political_divisions_of_the_United_States';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)
for tr in root.cssselect("table.multicol ul"):
    for num in range(0,10):
        print 'Saving data for ' + tr[num].text_content() + '...'
        city = re.findall('^[\w\s]*', tr[num].text_content())
        #print city
        abbr = re.findall('\([A-Z]*\)', tr[num].text_content())
        data = {"City":''.join(city),"Abbreviation":''.join(abbr).strip("()")}
        scraperwiki.sqlite.save(["City"], data)



"""
print 'Geocoding locations...'

locations = scraperwiki.sqlite.select("* from cities where longitude='' order by city")

for location in locations:
    print 'Geocoding ' + location['city'] + '...'
    raw_json = scraperwiki.scrape('http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=' + urllib.quote(location['city'].encode('utf-8')) + ',+CA')
    geo_object = json.loads(raw_json)
    lat = geo_object['results'][0]['geometry']['location']['lat']
    lng = geo_object['results'][0]['geometry']['location']['lng']
    print 'Saving ' + location['city'] + '...'
    scraperwiki.sqlite.execute('update cities set latitude="' + str(lat) + '", longitude="' + str(lng) + '" where city="' + location['city'] + '"')
    scraperwiki.sqlite.commit()
"""