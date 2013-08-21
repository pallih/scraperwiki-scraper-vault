# Estrai utenti
import scraperwiki
import simplejson
import urllib2

# since:2012-04-12 until:2012-04-13
QUERY = 'bersagliomobile'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'it'
NUM_PAGES = 15

# nota: puoi estrarre circa 1500 tweets. è meglio usare 10 pagine per volta
# e poi partire dall'ultimo tweet estratto aggiungendo in base_url
# il parametro &max_id=ID-ULTIMO-TWEET
for page in range(1, NUM_PAGES+1):
    base_url = 'https://api.twitter.com/1.1/search/tweets.json?q=%s&count=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['from_user'] = result['from_user']
            scraperwiki.sqlite.save(["from_user"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    