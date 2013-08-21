import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
import json
import re
import urllib


'''
index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_Occupy_movement_protest_locations';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

print 'Extracting HTML...'
print html

root = lxml.html.fromstring(html)

for table in root.cssselect("table.wikitable.sortable"):

    print table.text_content()
    if(len(table.getprevious().cssselect('.mw-headline'))):
        continent = table.getprevious().cssselect('.mw-headline a')[0].text_content()
    elif(len(table.getprevious().cssselect('.rellink'))):
        continent = table.getprevious().getprevious().cssselect('.mw-headline a')[0].text_content()
    else:
        continent = '(unknown)'
    
    print 'Scraping protests in: ' + continent + '...'

    for tr in table.cssselect('tr'):
        if(len(tr.cssselect("td")) and tr[0].text_content() != ""):
            if(len(tr.cssselect('td')) == 6):
                # tr.cssselect('td')[0] will be a country name
                country = tr.cssselect('td')[0].text_content()
                regexp = re.search('^([^-]+)', country)
                if(regexp):
                    country = regexp.group(1).strip()
                city = tr.cssselect('td')[1].text_content()
                date = tr.cssselect('td')[2].text_content()
                people = tr.cssselect('td')[3].text_content()
            elif(len(tr.cssselect('td')) == 5):
                # tr.cssselect('td')[0] will be a city
                city = tr.cssselect('td')[0].text_content()
                date = tr.cssselect('td')[1].text_content()
                people = tr.cssselect('td')[2].text_content()
            if(city):
                location = city + ', ' + country
            else:
                location = country
            print "Saving data for " + location + '...'
            scraperwiki.sqlite.save(unique_keys=["location"], data={"location": location, "contintent": continent, "country": country, "city": city, "start_date": date, "estimated_attendance": people, "latitude":'', "longitude":''}, table_name="locations")

'''

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



