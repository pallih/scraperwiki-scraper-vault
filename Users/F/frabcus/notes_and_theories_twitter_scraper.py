# Grab links from #nt people that use Twitter instead of Delicious for link sharing
# Only keeps tweets with an http/https URL in them, and that aren't @ another user.

import scraperwiki
import simplejson
import urllib2
import dateutil.parser
import sys

# Add new people to this list:
usernames = ['frabcus',
             'domfox',
             'mhl20',
             'sc3d',
             'darkgreener',
             'tmrooke',
             'steiny',
             'colourcountry',
             'eyebrowsofpower']

QUERY = ' OR '.join('from:' + u for u in usernames)
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 1

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            # only grab things with links
            if "http://" not in result['text'] and "https://" not in result['text']:
                continue
            # only grab things that aren't to a particular user
            if result['to_user_name'] != None:
                continue
            print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = dateutil.parser.parse(result['created_at'])
            
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print 'Oh dear, failed to scrape %s' % base_url
