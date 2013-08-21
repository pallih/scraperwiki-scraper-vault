###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
# as used by elana for her final project
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '#muckedup'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 1 

# a URL template for retrieving information about a Tweet;
# includes a placeholder for the Tweet ID
tweet_info_url = 'http://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true'

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
            
            # make a request for the tweet info
            try:
                tweet_info = simplejson.loads(scraperwiki.scrape(tweet_info_url % data['id']))
                data['retweet_count'] = tweet_info['retweet_count']
            except:
                print 'Failed to retrieve information for tweet #', data['id']
            
            print data['from_user'], data['text'], data['retweet_count']
            scraperwiki.sqlite.save(["id"], data) 
            
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    