###############################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###############################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'navidad'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'es'
NUM_PAGES = 15
UNTIL = '2012-12-09'
RESULT_TYPE = 'recent'
MAX_ID= 277562601750290433

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&until=%s&result_type=%s&max_id=%s' \
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page, UNTIL, RESULT_TYPE, MAX_ID)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['retweet_count'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text'] 
            scraperwiki.sqlite.save(["id"], data)
            
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    

###############################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###############################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'navidad'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'es'
NUM_PAGES = 15
UNTIL = '2012-12-09'
RESULT_TYPE = 'recent'
MAX_ID= 277562601750290433

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&until=%s&result_type=%s&max_id=%s' \
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page, UNTIL, RESULT_TYPE, MAX_ID)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['retweet_count'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text'] 
            scraperwiki.sqlite.save(["id"], data)
            
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    

