#######################################################################################################################
# Twitter API scraper - Scrapping twitter for dataset to be used for sentiment analysis and data visualization         
#######################################################################################################################

import scraperwiki
import simplejson
import urllib2
import time


QUERY = 'jellybean OR blackberry OR ios OR android OR windows OR Apple OR iphone OR galaxys3 OR galaxys4'
GEOINFO = '91.26521293124656,-91.063720703125,257km'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15
error_count = 0

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            scraperwiki.sqlite.save(["id"], data)
            print scraperwiki.sqlite.Rows, data['from_user'], data['text'];
            error_count = 0
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        #print err
        error_count = error_count+1
        if error_count > 7:
            print "sleeping"
            time.sleep(300)
            print "woke up"
            error_count = 0
