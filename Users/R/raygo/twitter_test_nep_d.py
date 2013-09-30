###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'neuropathic pain OR shingles pain OR zoster pain OR post-shingles pain OR postherpetic neuralgia OR postherpetic pain OR diabetic neuropathic pain OR diabetic neuropathy OR diabetic polyneuropathy OR herpes zoster OR diabetic pain'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

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
            data['created_at'] = result['created_at']
            print data['from_user'], data['text'], data['created_at']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    ###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = 'neuropathic pain OR shingles pain OR zoster pain OR post-shingles pain OR postherpetic neuralgia OR postherpetic pain OR diabetic neuropathic pain OR diabetic neuropathy OR diabetic polyneuropathy OR herpes zoster OR diabetic pain'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 15 

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
            data['created_at'] = result['created_at']
            print data['from_user'], data['text'], data['created_at']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    