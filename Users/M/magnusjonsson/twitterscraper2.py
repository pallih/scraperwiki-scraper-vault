import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'society6'
RESULTS_PER_PAGE = '9000'
LANGUAGE = 'en'
NUM_PAGES = 10000

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}          
            data['text'] = result['text']
            data ['div.chk'] = result ['div.chk']
            print data['text']
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'society6'
RESULTS_PER_PAGE = '9000'
LANGUAGE = 'en'
NUM_PAGES = 10000

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}          
            data['text'] = result['text']
            data ['div.chk'] = result ['div.chk']
            print data['text']
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    