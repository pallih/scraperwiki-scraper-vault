import scraperwiki
import simplejson
import urllib2


QUERY = 'apple AND news'
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'https://mobile.twitter.com/' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
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
        print 'Oh dear, failed to scrape %s' % base_urlimport scraperwiki
import simplejson
import urllib2


QUERY = 'apple AND news'
GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

for page in range(1, NUM_PAGES+1):
    base_url = 'https://mobile.twitter.com/' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
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