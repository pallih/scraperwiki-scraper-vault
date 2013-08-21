###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import time
import datetime

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = ('FTSE', 'obama')
RESULTS_PER_PAGE = '100'
NUM_PAGES = 300

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text'].replace("&quot;", "'")
            data['from_user'] = result['from_user']
            data['lang'] = result['iso_language_code']
            data['date'] = datetime.datetime(*time.strptime(result['created_at'], '%a, %d %b %Y %H:%M:%S +0000')[:6])
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except Exception, e:
        print e
        print 'Oh dear, failed to scrape %s' % base_url
    