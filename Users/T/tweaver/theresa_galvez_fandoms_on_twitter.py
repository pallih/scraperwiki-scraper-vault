###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2


QUERY = '#doctorwho'
QUERY = '#harrypotter'
QUERY = '#hungergames'
QUERY = '#lotr OR #lordoftherings'
QUERY = '#starwars'
QUERY = '#twilight'
QUERY = '#gameofthrones'
QUERY = '#theavengers'
QUERY = '#ladygaga'
QUERY = '#lilb'
QUERY = '#beliebers'
GEOINFO = '40.4230,-98.7372,2317km'
RESULTS_PER_PAGE = '100'
RESULT_TYPE = 'mixed'
LANGUAGE = 'en'
NUM_PAGES = 100 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&geocode=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), urllib2.quote(GEOINFO), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    