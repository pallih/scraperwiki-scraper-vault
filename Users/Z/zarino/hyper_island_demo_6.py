# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
        r = requests.get('https://scraperwiki.com/about/', verify=False).text
        dom = lxml.html.fromstring(r)
        for person in dom.cssselect('#team h3'):
            d = {
                'name': person.cssselect('a')[0].text,
                'job': person.cssselect('small')[0].text.replace('\xa0', ' ')
            }
            print d

scrape_people()# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
        r = requests.get('https://scraperwiki.com/about/', verify=False).text
        dom = lxml.html.fromstring(r)
        for person in dom.cssselect('#team h3'):
            d = {
                'name': person.cssselect('a')[0].text,
                'job': person.cssselect('small')[0].text.replace('\xa0', ' ')
            }
            print d

scrape_people()