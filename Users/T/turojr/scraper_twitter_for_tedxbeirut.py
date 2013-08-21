###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'salvaciclisti'
GEOINFO = ''
UNTIL=''
RESULTS_PER_PAGE = '300'

NUM_PAGES = 200 
ENTITY = 'true'


for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&until=%s&rpp=%s&lang=%s&page=%s=include_entities=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page, urllib2.quote(ENTITY))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['to_user'] = result['to_user']
            data['geo'] = result['geo']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    