import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice. 
QUERY = 'Conservative Party Canada'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 50 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['date'] = result['created_at']
            data['from_user'] = result['from_user']
            scraperwiki.sqlite.save(["id"], data)
            print data['from_user'],",", data['text']
    except:
        pass