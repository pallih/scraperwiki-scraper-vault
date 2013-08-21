import scraperwiki
import simplejson
import urllib2
import time
import datetime

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = ('kersfees')
RESULTS_PER_PAGE = '100'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):
    print page
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text'].replace("&quot;", "'")
            data['from_user'] = result['from_user']
            data['date'] = datetime.datetime(*time.strptime(result['created_at'], '%a, %d %b %Y %H:%M:%S +0000')[:6])
            
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'failed to scrape %s' % base_url

