###############################################################################
# Basic scraper propertywala
###############################################################################

import scraperwiki
import datetime
import re
import time
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    #html = scraperwiki.scrape(starting_url)
    #soup = BeautifulSoup(html)
    #print html
    recs = "2 hours ago"
    token = recs.split()
    if token[1] == 'days':
        print long( time.time() - int(token[0])*1000*60*60*24)
    print long( time.time())

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-new_delhi'
scrape_post('Delhi',starting_url)###############################################################################
# Basic scraper propertywala
###############################################################################

import scraperwiki
import datetime
import re
import time
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    #html = scraperwiki.scrape(starting_url)
    #soup = BeautifulSoup(html)
    #print html
    recs = "2 hours ago"
    token = recs.split()
    if token[1] == 'days':
        print long( time.time() - int(token[0])*1000*60*60*24)
    print long( time.time())

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-new_delhi'
scrape_post('Delhi',starting_url)