# Estrai cinguettii
import scraperwiki
import simplejson
import urllib2

# since:2012-04-12 until:2012-04-13
QUERY = '#piazzapulita'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'it'
NUM_PAGES = 13

# nota: puoi estrarre circa 1500 tweets. è meglio usare 10 pagine per volta
# e poi partire dall'ultimo tweet estratto aggiungendo in base_url
# il parametro &max_id=ID-ULTIMO-TWEET
for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent&max_id=200679262997585921' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    # Estrai cinguettii
import scraperwiki
import simplejson
import urllib2

# since:2012-04-12 until:2012-04-13
QUERY = '#piazzapulita'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'it'
NUM_PAGES = 13

# nota: puoi estrarre circa 1500 tweets. è meglio usare 10 pagine per volta
# e poi partire dall'ultimo tweet estratto aggiungendo in base_url
# il parametro &max_id=ID-ULTIMO-TWEET
for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent&max_id=200679262997585921' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    