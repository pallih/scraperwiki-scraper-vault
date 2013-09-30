###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'


QUERY = ''
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 1000 

for page in range(1, NUM_PAGES+1):

    base_url = 'http://search.twitter.com/search.json?geocode=51.316667,9.5,40mi' 

    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['from_user_name'] = result['from_user_name']
            data['created_at'] = result['created_at']
            data['to_user'] = result['to_user']
            data['geo'] = result['geo']       
            data['lang'] = result['iso_language_code']    
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'


QUERY = ''
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 1000 

for page in range(1, NUM_PAGES+1):

    base_url = 'http://search.twitter.com/search.json?geocode=51.316667,9.5,40mi' 

    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['from_user_name'] = result['from_user_name']
            data['created_at'] = result['created_at']
            data['to_user'] = result['to_user']
            data['geo'] = result['geo']       
            data['lang'] = result['iso_language_code']    
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
