# All UK Towns and Cities and their coordinates
# Based on a scraper written by Ross Jones

# Town and City names scraped from Wikipedia:
# http://en.wikipedia.org/wiki/List_of_towns_in_the_United_Kingdom
# http://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom
# Towns and Cities geolocated by the Geonames API

import scraperwiki
import lxml.html
from urllib import urlencode
import json
import re


# helper functions

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

def scrape_locations():

    locations = []
    cities = [] # we keep a note of cities, to avoid duplicates from the towns pages (stupid Wikipedia)
    
    print 'Scraping cities...'
    
    cities_html = lxml.html.fromstring(get_html('Z-transform'))
    for table in cities_html.cssselect("table.wikitable.sortable"):
        country = table.getprevious().cssselect('.mw-headline')[0].text
        print '-- scraping cities in ' + country + '...'
        for tr in table.cssselect('tr'):
            if(len(tr.cssselect("td"))):
                name = tr.cssselect('td a')[0].text
                cities.append(name)
                locat       
    print locations
    
    print 'Done!'
    

scrape_locations()



# All UK Towns and Cities and their coordinates
# Based on a scraper written by Ross Jones

# Town and City names scraped from Wikipedia:
# http://en.wikipedia.org/wiki/List_of_towns_in_the_United_Kingdom
# http://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom
# Towns and Cities geolocated by the Geonames API

import scraperwiki
import lxml.html
from urllib import urlencode
import json
import re


# helper functions

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

def scrape_locations():

    locations = []
    cities = [] # we keep a note of cities, to avoid duplicates from the towns pages (stupid Wikipedia)
    
    print 'Scraping cities...'
    
    cities_html = lxml.html.fromstring(get_html('Z-transform'))
    for table in cities_html.cssselect("table.wikitable.sortable"):
        country = table.getprevious().cssselect('.mw-headline')[0].text
        print '-- scraping cities in ' + country + '...'
        for tr in table.cssselect('tr'):
            if(len(tr.cssselect("td"))):
                name = tr.cssselect('td a')[0].text
                cities.append(name)
                locat       
    print locations
    
    print 'Done!'
    

scrape_locations()



