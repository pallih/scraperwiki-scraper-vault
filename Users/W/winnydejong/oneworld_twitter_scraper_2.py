import scraperwiki
import simplejson
import urllib2
import datetime

# Change QUERY to your search term of choice.
# I've set the query for several OneWorld hashtags, as well as mentions of OneWorld
QUERY = '#oneworld OR #oneworld.nl OR #oneworldnl OR to:oneworldnl'
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text'].replace("&quot;", "'")
            data['from_user'] = result['from_user']
            data['geo'] = result['geo']
            data['source'] = result['source']
            data['iso_language_code'] = result['iso_language_code']
            data['from_user_name'] = result['from_user_name']
            data['date'] = datetime.datetime.today()
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    import scraperwiki
import simplejson
import urllib2
import datetime

# Change QUERY to your search term of choice.
# I've set the query for several OneWorld hashtags, as well as mentions of OneWorld
QUERY = '#oneworld OR #oneworld.nl OR #oneworldnl OR to:oneworldnl'
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text'].replace("&quot;", "'")
            data['from_user'] = result['from_user']
            data['geo'] = result['geo']
            data['source'] = result['source']
            data['iso_language_code'] = result['iso_language_code']
            data['from_user_name'] = result['from_user_name']
            data['date'] = datetime.datetime.today()
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    