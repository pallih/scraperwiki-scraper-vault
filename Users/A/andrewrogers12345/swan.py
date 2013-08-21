###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice.
# Examples: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
#QUERY = '#sunderlandfc'
#QUERY = '#cfc'
#QUERY = '#mufc'
#QUERY = '#arsenalfc'
#QUERY = '#evertonfc'
#QUERY = '#lfc'
#QUERY = '#qpr'
#QUERY = '#whufc'
#QUERY = '#nufc'
#QUERY = '#ncfc'
QUERY = '#swans'
#QUERY = '#scfc'
#QUERY = '#mcfc'
#QUERY = '#thfc'
#QUERY = '#avfc'
#QUERY = '#wbafc'
#QUERY = '#readingfc'
#QUERY = '#saintsfc'
#QUERY = '#wigan'
#QUERY = '#ffc'

RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 100


for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=exclude:retweets+%s&rpp=%s&lang=%s&page=%s&geocode=51.50019435946635,-0.12359619140625,25mi' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['geo'] = result['geo']
            data['profile_image_url'] = result['profile_image_url']
            data['from_user_id_str'] = result['from_user_id_str']
            data['created_at'] = result['created_at']
            data['from_user'] = result['from_user']
            data['id_str'] = result['id_str']
            data['metadata'] = result['metadata']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url