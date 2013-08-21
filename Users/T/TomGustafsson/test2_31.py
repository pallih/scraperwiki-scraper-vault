# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
    r = requests.get('http://www.hyperisland.com/people?filter=true&role=student').text
    dom = lxml.html.fromstring(r)

scrape_people()

