###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

import dateutil.parser as parser

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'

QUERY = 'OCHA'  
RESULTS_PER_PAGE = '100'
#LANGUAGE = 'en'
NUM_PAGES = 1000

for page in range(1, NUM_PAGES+1):
#    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
#         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['from_user_name'] = result['from_user_name']
            data['from_user_id'] = result['from_user_id']
            data['iso_language_code'] = result['iso_language_code']

            data['profile_image_url'] = result['profile_image_url']
            data['to_user'] = result['to_user']
            data['to_user_id'] = result['to_user_id']
            data['from_user'] = result['from_user']
            data['geo'] = result['geo']
            #data['in_reply_to_status_id'] = result['in_reply_to_status_id']
            data['source'] = result['source']
            data['created_at'] = result['created_at']
            createdAT = parser.parse( result['created_at'] )
            data['created_iso'] =  createdAT.isoformat()
            print data['created_iso'] 
            #print data['iso_language_code'], "  ",  data['from_user'], data['text']
            print data['iso_language_code'], "...",data['created_at'], "...", data ['created_iso']
            #print result
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
