import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

# Develop a more accurate listing for the prelimanary scrape. 
format="json"
scraperName = "craigslist_flagger_2"
scrapes = BeautifulSoup( scraperwiki.scrape( 'http://api.scraperwiki.com/api/1.0/datastore/getdata?format=' + format + '&name=' + scraperName + '&limit=2') )
for scrapesJSON in scrapes:
    for scrape in json.loads( scrapesJSON ):            
        if scrape and scrape['link']:
            print "loading ..." + scrape['link']
            page = BeautifulSoup( scraperwiki.scrape( scrape['link']) )
            print page

