import scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'bbry'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 10
SINCE = '2013-03-15'
UNTIL= '2013-03-16'

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&lang=%s&since=%s&until=%s' \
         % (urllib2.quote(QUERY),RESULTS_PER_PAGE, page, LANGUAGE,SINCE, UNTIL)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_urlimport scraperwiki
import simplejson
import urllib2

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'bbry'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 10
SINCE = '2013-03-15'
UNTIL= '2013-03-16'

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&lang=%s&since=%s&until=%s' \
         % (urllib2.quote(QUERY),RESULTS_PER_PAGE, page, LANGUAGE,SINCE, UNTIL)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url