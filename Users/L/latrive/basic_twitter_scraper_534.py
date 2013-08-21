###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import datetime

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'PCC "Police Commissioner"
QUERY = 'latrive'
RESULTS_PER_PAGE = '10'
LANGUAGE = 'fr'
NUM_PAGES = 1 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        total = 0
        for result in results_json['results']:
            total = total+1
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            zetweettime = data['created_at']
            orbi = datetime.datetime.utcnow()
            print orbi
            print zetweettime
            zetweettime_date = datetime.datetime.strptime(zetweettime,"%a, %d %b %Y %H:%M:%S +0000")
            dif = orbi - zetweettime_date
            print dif
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
        print total
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    