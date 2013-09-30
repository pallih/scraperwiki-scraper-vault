import scraperwiki
import simplejson
import urllib2
QUERY = 'happy+OR+:)'
RESULTS_PER_PAGE = '100'
# LANGUAGE = 'en'
NUM_PAGES = 1 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&include_entities=true&geocode=59.326780,18.068390,25mi' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        print base_url
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            # print result
            print result
            data = {}
            data['id'] = result['id']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            if(result['geo']):
                data['lat'] = result['geo']['coordinates'][0]
                data['lng'] = result['geo']['coordinates'][1]
            print data['from_user']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        breakimport scraperwiki
import simplejson
import urllib2
QUERY = 'happy+OR+:)'
RESULTS_PER_PAGE = '100'
# LANGUAGE = 'en'
NUM_PAGES = 1 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&include_entities=true&geocode=59.326780,18.068390,25mi' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        print base_url
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            # print result
            print result
            data = {}
            data['id'] = result['id']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            if(result['geo']):
                data['lat'] = result['geo']['coordinates'][0]
                data['lng'] = result['geo']['coordinates'][1]
            print data['from_user']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break