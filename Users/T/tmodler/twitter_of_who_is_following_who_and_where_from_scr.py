###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import sys

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '@johnwarrillow'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 5
# Change GEOCODE to the location you want the user tweeting to be at
GEOCODE=('40.034557','-75.514396','50mi') # lat,lon,distance - 50 miles of Malvern, PA

for page in range(1, NUM_PAGES+1):
    # See http://search.twitter.com/api/ for help on Twitter Search API
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&geocode=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page, '%2C'.join(GEOCODE))

    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        print results_json
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    