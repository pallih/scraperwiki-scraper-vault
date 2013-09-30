###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'art AND gentrification'
#QUERY = 'beer'
##GEOINFO = '40.71427,-74.00597,35km' #new york
GEOINFO = '51.50722,-0.12750,35km' #london
##GEOINFO = '53.26521293124656,-9.063720703125,257km'

RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result['text']
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    ###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'art AND gentrification'
#QUERY = 'beer'
##GEOINFO = '40.71427,-74.00597,35km' #new york
GEOINFO = '51.50722,-0.12750,35km' #london
##GEOINFO = '53.26521293124656,-9.063720703125,257km'

RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result['text']
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    