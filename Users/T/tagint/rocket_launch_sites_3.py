# All UK Towns and Cities and their coordinates
# Based on a scraper written by Ross Jones

# Town and City names scraped from Wikipedia:
# http://en.wikipedia.org/wiki/List_of_towns_in_the_United_Kingdom
# http://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom
# Towns and Cities geolocated by the Geonames API
# In progress
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

    #spans = cities_html.xpath('.//tr/td/span[@class="longitude"]')
    #print spans[0].text

    # works to select span
    #for tag in cities_html.xpath('//*[self::span]'):
        #print(tag).text

    #for table in cities_html.cssselect("table.wikitable.sortable"):
    idfld = 0
    for table in cities_html.cssselect("table.wikitable"):
        #print "1"
        #continent = table.getprevious().cssselect('.mw-headline')[0].text
        #print '-- scraping cities in ' + continent + '...'
        for tr in table.cssselect('tr'):
            #print "2"
            #country = tr.cssselect('td')[0].text
            #print tr
            if(len(tr.cssselect("td"))):
                idfld += 1
                #print len(tr.cssselect("td"))
                country = tr.cssselect("td")[0].text
                
                name = tr.cssselect('td a')[0].text
                #print len(tr.xpath('td//div[@class="latitude"]'))
                #This works to select latitude in table row
                
                latitude = ""
                longitude = ""
                #if(len(tr.cssselect("span.latitude")[0].text)):
                if(tr.cssselect("span.latitude")):
                    latitude = tr.cssselect("span.latitude")[0].text
                #print tr.cssselect("span.latitude")[0].text
                if(tr.cssselect("span.longitude")):
                #if(len(tr.cssselect("span.longitude")[0].text)):
                    longitude = tr.cssselect("span.longitude")[0].text
                
                #select latitude / longitude by text length
                #if(len(tr.cssselect('td span')[3].text)) == 10:
                #    latitude = tr.cssselect('td span')[3].text
                #if(len(tr.cssselect('td span')[4].text)) == 10:
                #    longitude = tr.cssselect('td span')[4].text
                #print cities_html.xpath('//span[@class="graytext" and @style="font-size: 11px"]/text()')[0]
                #name2 = tr.cssselect('td a')[1].text
                #name3 = tr.cssselect('td a')[2].text
                #name4 = tr.cssselect('td a')[3].text
                
                print country
                print name
                #print len(tr.cssselect("td"))
                print latitude
                print longitude 
                #cities.append(name)
                locations.append({'idfld':idfld,'name': name, 'country': country, 'latitude': latitude, 'longitude': longitude})
    
    
        
    print locations
    
    scraperwiki.sqlite.save(["idfld"], locations, "rocket launch sites")

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
#geocode_locations()



# All UK Towns and Cities and their coordinates
# Based on a scraper written by Ross Jones

# Town and City names scraped from Wikipedia:
# http://en.wikipedia.org/wiki/List_of_towns_in_the_United_Kingdom
# http://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom
# Towns and Cities geolocated by the Geonames API
# In progress
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

    #spans = cities_html.xpath('.//tr/td/span[@class="longitude"]')
    #print spans[0].text

    # works to select span
    #for tag in cities_html.xpath('//*[self::span]'):
        #print(tag).text

    #for table in cities_html.cssselect("table.wikitable.sortable"):
    idfld = 0
    for table in cities_html.cssselect("table.wikitable"):
        #print "1"
        #continent = table.getprevious().cssselect('.mw-headline')[0].text
        #print '-- scraping cities in ' + continent + '...'
        for tr in table.cssselect('tr'):
            #print "2"
            #country = tr.cssselect('td')[0].text
            #print tr
            if(len(tr.cssselect("td"))):
                idfld += 1
                #print len(tr.cssselect("td"))
                country = tr.cssselect("td")[0].text
                
                name = tr.cssselect('td a')[0].text
                #print len(tr.xpath('td//div[@class="latitude"]'))
                #This works to select latitude in table row
                
                latitude = ""
                longitude = ""
                #if(len(tr.cssselect("span.latitude")[0].text)):
                if(tr.cssselect("span.latitude")):
                    latitude = tr.cssselect("span.latitude")[0].text
                #print tr.cssselect("span.latitude")[0].text
                if(tr.cssselect("span.longitude")):
                #if(len(tr.cssselect("span.longitude")[0].text)):
                    longitude = tr.cssselect("span.longitude")[0].text
                
                #select latitude / longitude by text length
                #if(len(tr.cssselect('td span')[3].text)) == 10:
                #    latitude = tr.cssselect('td span')[3].text
                #if(len(tr.cssselect('td span')[4].text)) == 10:
                #    longitude = tr.cssselect('td span')[4].text
                #print cities_html.xpath('//span[@class="graytext" and @style="font-size: 11px"]/text()')[0]
                #name2 = tr.cssselect('td a')[1].text
                #name3 = tr.cssselect('td a')[2].text
                #name4 = tr.cssselect('td a')[3].text
                
                print country
                print name
                #print len(tr.cssselect("td"))
                print latitude
                print longitude 
                #cities.append(name)
                locations.append({'idfld':idfld,'name': name, 'country': country, 'latitude': latitude, 'longitude': longitude})
    
    
        
    print locations
    
    scraperwiki.sqlite.save(["idfld"], locations, "rocket launch sites")

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
#geocode_locations()



