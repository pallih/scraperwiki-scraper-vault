# Blank Python

import scraperwiki
import simplejson
import urllib2


QUERY = 'referendum'
# GEOINFO = '53.26521293124656,-9.063720703125,257km'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'fr'
NUM_PAGES = 150 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['created_at'] = result['created_at']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print str(page) + 'SCRAPED PAGES FAIL'
        break
