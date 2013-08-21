###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'Cegedim'
RESULTS_PER_PAGE = '15'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']

#            ll = result['geo']
#
#            for item in ll:
#
#                if item.has_key('coordinates'):
#                    data['geoloc'] = item['coordinates']

            data['coordinates'] = result['geo']['coordinates']
            print data['from_user'], data['text'], data['created_at'], data['coordinates']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        