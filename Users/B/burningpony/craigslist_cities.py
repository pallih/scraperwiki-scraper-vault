###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( 'http://www.craigslist.org/about/sites' ) )
for li in soup('li'):

    if li.a:

        record ={}
        record['title'] = li.a.text
        record['state'] = li.findPrevious('div').text
        record['continent'] = li.findPrevious('h1').text

        if li.a['href']:
            record['link'] = li.a['href']
            scraperwiki.sqlite.save( ["link"] , record )
            print record
                
###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( 'http://www.craigslist.org/about/sites' ) )
for li in soup('li'):

    if li.a:

        record ={}
        record['title'] = li.a.text
        record['state'] = li.findPrevious('div').text
        record['continent'] = li.findPrevious('h1').text

        if li.a['href']:
            record['link'] = li.a['href']
            scraperwiki.sqlite.save( ["link"] , record )
            print record
                
