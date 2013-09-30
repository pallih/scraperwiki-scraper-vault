#########################################
# Twitter API scraper - Nicholas Chimonas
#########################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'SEO'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
% (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, 1)  
try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
except:
        print 'Oh dear, failed to scrape %s' % base_url#########################################
# Twitter API scraper - Nicholas Chimonas
#########################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'SEO'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
% (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, 1)  
try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
except:
        print 'Oh dear, failed to scrape %s' % base_url