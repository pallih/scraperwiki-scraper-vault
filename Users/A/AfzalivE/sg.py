'''
Created on Apr 30, 2013

@author: afzal
'''
import scraperwiki
import simplejson
import sys
import urllib2

RESULTS_PER_PAGE = '10'
LANGUAGE = 'en'
NUM_PAGES = 1

TNAME = 'nba'

for page in range(1, NUM_PAGES+1):
    base_url = 'http://api.seatgeek.com/2/events?taxonomies.name=%s' \
        % (urllib2.quote(TNAME))
#     base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
#          % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['events']:
            data = {}
            data['id'] = result['id']
            data['short_title'] = result['short_title']
            data['datetime_utc'] = result['datetime_utc']
            data['name'] = result['venue']['name']

            print data
            scraperwiki.sqlite.save(["id"], data)
    except:
        print sys.exc_info()[0]
        print 'Oh dear, failed to scrape %s' % base_url