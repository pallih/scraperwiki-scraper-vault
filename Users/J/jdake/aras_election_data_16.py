###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'kroning'

GEOINFO = '52.090142,5.109665,200km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'nl'
NUM_PAGES = 1

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['profile_image_url'] = result['profile_image_url']
            data['geo'] = result['geo']
            #data['media'] = result['media']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    ###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'kroning'

GEOINFO = '52.090142,5.109665,200km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'nl'
NUM_PAGES = 1

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['profile_image_url'] = result['profile_image_url']
            data['geo'] = result['geo']
            #data['media'] = result['media']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    