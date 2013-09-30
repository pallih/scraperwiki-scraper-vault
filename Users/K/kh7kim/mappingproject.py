###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'beatmaker OR blackberry10'
GEOINFO = '43.723475,-79.417648,1500km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            scraperwiki.sqlite.save(["id"], result)
    except:
        print 'Oh dear, failed to scrape %s' % base_url###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'beatmaker OR blackberry10'
GEOINFO = '43.723475,-79.417648,1500km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            scraperwiki.sqlite.save(["id"], result)
    except:
        print 'Oh dear, failed to scrape %s' % base_url