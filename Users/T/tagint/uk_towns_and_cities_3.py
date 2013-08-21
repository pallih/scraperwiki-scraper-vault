# All UK Towns and Cities and their coordinates
# Based on a scraper written by Ross Jones

# Town and City names scraped from Wikipedia:
# http://en.wikipedia.org/wiki/List_of_towns_in_the_United_Kingdom
# http://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom
# Towns and Cities geolocated by the Geonames API
# Template that works !
import scraperwiki
import lxml.html
from urllib import urlencode
import json
import re



# helper functions

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    print html
    return html

def geocode_location(name):
    u = urlencode({ 'username':'scraperwiki', 'maxRows':1, 'country': 'gb', 'q': name })
    result = scraperwiki.scrape( "http://api.geonames.org/search?" + u )
    page = lxml.html.fromstring( result )
    return [page.cssselect('lat')[0].text_content(), page.cssselect('lng')[0].text_content()]


def scrape_locations():

    locations = []
    cities = [] # we keep a note of cities, to avoid duplicates from the towns pages (stupid Wikipedia)
    
    print 'Scraping cities...'
    
    #cities_html = lxml.html.fromstring(get_html('List_of_cities_in_the_United_Kingdom'))
    cities_html = lxml.html.fromstring(get_html('List_of_rocket_launch_sites'))
    #for table in cities_html.cssselect("table.wikitable.sortable"):
    for table in cities_html.cssselect("table.wikitable"):
        #print "1"
        #continent = table.getprevious().cssselect('.mw-headline')[0].text
        #print '-- scraping cities in ' + continent + '...'
        for tr in table.cssselect('tr'):
            #print "2"
            #country = tr.cssselect('td')[0].text
            #print tr
            if(len(tr.cssselect("td"))):
                print "3"
                name = tr.cssselect('td a')[0].text
                #name2 = tr.cssselect('td a')[1].text
                #name3 = tr.cssselect('td a')[2].text
                #name4 = tr.cssselect('td a')[3].text
                print name
                #cities.append(name)
                #locations.append({'name': name, 'country': country, 'type': 'city'})
    
    
        
    print locations
    
    #scraperwiki.sqlite.save(['name','country'], locations, 'towns_and_cities')

    print 'Done!'
    


def geocode_locations():
    
    try:
        locations = scraperwiki.sqlite.select('* from towns_and_cities where lat is null order by name')
    except:
        locations = scraperwiki.sqlite.select('* from towns_and_cities order by name')

    print 'Geocoding ' + str(len(locations)) + ' locations...'

    geocoded = []
    for location in locations:
        temp = location
        try:
            latlng = geocode_location(location['name'])
            temp['lat'] = float(latlng[0])
            temp['lng'] = float(latlng[1])
        except:
            if re.search('and', location['name']) or re.search('&', location['name']):
                print '-- Could not geocode ' + location['name'] + '. Trying ' + location['name'].split(' ')[0] + '...'
                try:
                    latlng = geocode_location(location['name'].split(' ')[0])
                    temp['lat'] = float(latlng[0])
                    temp['lng'] = float(latlng[1])
                except:
                    print '-- Could not geocode ' + location['name'].split(' ')[0]
            else:
                print '-- Could not geocode ' + location['name']

        geocoded.append(temp)

    print 'Saving geocoded locations...'

    print geocoded

    scraperwiki.sqlite.save(['name','country'], geocoded, 'towns_and_cities')

    print 'Done!'


scrape_locations()
geocode_locations()



