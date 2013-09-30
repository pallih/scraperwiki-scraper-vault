###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'labiennale'
RESULTS_PER_PAGE = '100'
COORDINATES = '45.437129,12.333498'
RADIUS = '3mi'
RESULT_TYPE = 'mixed'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):
    base_url = 'https://twitter.com/search/realtime?q=vine.co%2Fv%2F&geocode=%s,%s&result_type=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page,COORDINATES,RADIUS,RESULT_TYPE)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break


import scraperwiki

# Blank Python




###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'labiennale'
RESULTS_PER_PAGE = '100'
COORDINATES = '45.437129,12.333498'
RADIUS = '3mi'
RESULT_TYPE = 'mixed'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):
    base_url = 'https://twitter.com/search/realtime?q=vine.co%2Fv%2F&geocode=%s,%s&result_type=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page,COORDINATES,RADIUS,RESULT_TYPE)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break


import scraperwiki

# Blank Python




