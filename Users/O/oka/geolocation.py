import scraperwiki
import simplejson
import urllib2
import datetime
import cgi
import os

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'

# http://search.twitter.com/search.json?q=social%20media&geocode=55.00839,-5.822485,1145.0km&rpp=100

qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
QUERY = '59,10,10km'

RESULTS_PER_PAGE = '100000'
NUM_PAGES = 5 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?geocode=%s' % (QUERY)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text'].replace("&quot;", "'")
            data['from_user'] = result['from_user']
            data['date'] = datetime.datetime.today()
            data['location'] = result['location']
            data['source'] = result['source']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    
# Blank Python
