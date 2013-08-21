###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice.
# Examples: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '"I will not vote" -"EMA" -"AMA" -"obama" -"@barackobama" -"#barackobama" -"romney" -"@mittromney" -"#mittromney" -"xfactor" -"x-factor" -"x factor" -"#xfactor" -"MTV" -"singer"'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 100


for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=exclude:retweets+%s&rpp=%s&lang=%s&page=%s' \
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
            data['to_user_id'] = result['to_user_id']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
