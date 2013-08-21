###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'sweden'
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 3000 

for page in range(1, NUM_PAGES+1):
    base_url = 'https://api.twitter.com/1.1/search/tweets.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['created_at'] = result['created_at']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['geo'] = result['geo']
            data['iso_language_code'] = result['iso_language_code']
            print data['from_user'], data['text'], data['created_at'], data['geo'], data['iso_language_code']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    