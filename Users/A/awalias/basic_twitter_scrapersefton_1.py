###################################################################################
# It appears that the number of 'goats teleported' by googles chromium browser has increased
# significantly (http://code.google.com/p/chromium/issues/detail?id=31482).
# It is important that we track down the original owners of the goats and reunite them where possible.  
###################################################################################

import scraperwiki
import simplejson
import urllib2

QUERY = '"missing goat"'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 1000 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    