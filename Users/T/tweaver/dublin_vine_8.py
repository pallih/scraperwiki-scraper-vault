###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'vine.co/v/'
GEOCODE = '53.347938,-6.258259,15Mi'


base_url = 'https://twitter.com/search?q=%s&GEOCODE%s' \
         % (urllib2.quote(QUERY), GEOCODE, )
try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)






###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'vine.co/v/'
GEOCODE = '53.347938,-6.258259,15Mi'


base_url = 'https://twitter.com/search?q=%s&GEOCODE%s' \
         % (urllib2.quote(QUERY), GEOCODE, )
try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text'], data['geo']
            scraperwiki.sqlite.save(["id"], data)






