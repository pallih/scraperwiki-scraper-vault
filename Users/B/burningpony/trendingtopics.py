###############################################################################
# Trending Topics scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( 'http://www.google.com/trends/hottrends?sa=X' ) )
for li in soup('td'):

        if li.a:

            record ={}
            record['title'] = li.a.text

            if li.a['href']:
                if re.search( r"/trends/hottrends\?.*" , li.a['href'] ):
                    record['link'] = li.a['href']
                    scraperwiki.sqlite.save( ["link"] , record )
                    print record
                
###############################################################################
# Trending Topics scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

# retrieve a page
soup = BeautifulSoup( scraperwiki.scrape( 'http://www.google.com/trends/hottrends?sa=X' ) )
for li in soup('td'):

        if li.a:

            record ={}
            record['title'] = li.a.text

            if li.a['href']:
                if re.search( r"/trends/hottrends\?.*" , li.a['href'] ):
                    record['link'] = li.a['href']
                    scraperwiki.sqlite.save( ["link"] , record )
                    print record
                
