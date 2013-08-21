import scraperwiki
import simplejson
import urllib2


QUERY = 'joiz OR #joiz OR @joiz'
RESULTS_PER_PAGE = '100'
#LANGUAGE = 'de'
NUM_PAGES = 15


for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print data['from_user'], data['text'], data['profile_image'],
            scraperwiki.sqlite.save(["id",], result, verbose=0)

    except:
        print 'Abgebrochen %s' % base_url

        
    
