import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'vine.co/v/'
RESULTS_PER_PAGE = '100'
COORDINATES = '51.50146119275354,-0.1906273812055'
RADIUS = '3mi'
RESULT_TYPE = 'mixed'
NUM_PAGES = 100 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&geocode=%s,%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page,COORDINATES,RADIUS)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            #data['coordinates'] = result['coordinates']
            #print data['from_user'], data['text'], data['geo']
            if data['geo'] is not None:
                print 'found some data' , data['geo']
            #if data['coordinates'] is not None:
                   #print 'found some coordinates' , data['coordinates']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break


import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'vine.co/v/'
RESULTS_PER_PAGE = '100'
COORDINATES = '51.50146119275354,-0.1906273812055'
RADIUS = '3mi'
RESULT_TYPE = 'mixed'
NUM_PAGES = 100 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&geocode=%s,%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page,COORDINATES,RADIUS)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['geo'] = result['geo']
            #data['coordinates'] = result['coordinates']
            #print data['from_user'], data['text'], data['geo']
            if data['geo'] is not None:
                print 'found some data' , data['geo']
            #if data['coordinates'] is not None:
                   #print 'found some coordinates' , data['coordinates']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break


