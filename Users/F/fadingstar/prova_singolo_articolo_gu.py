import scraperwiki
import time
import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
QUERY = 'http://www.guardian.co.uk/news/datablog/2012/sep/17/prison-probation-suicide-mapped'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):

    time.sleep(5)

    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&include_entities=true&page=%s'\
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    
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
            data['entities'] = result['entities']
            #for e in result['entities']['hashtags']:
                #print e['text']
            scraperwiki.sqlite.save(["id"], data) 

    except:
        break
        print 'Error with url: %s' % base_url
import scraperwiki
import time
import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
QUERY = 'http://www.guardian.co.uk/news/datablog/2012/sep/17/prison-probation-suicide-mapped'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):

    time.sleep(5)

    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&include_entities=true&page=%s'\
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    
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
            data['entities'] = result['entities']
            #for e in result['entities']['hashtags']:
                #print e['text']
            scraperwiki.sqlite.save(["id"], data) 

    except:
        break
        print 'Error with url: %s' % base_url
import scraperwiki
import time
import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
QUERY = 'http://www.guardian.co.uk/news/datablog/2012/sep/17/prison-probation-suicide-mapped'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):

    time.sleep(5)

    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&include_entities=true&page=%s'\
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    
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
            data['entities'] = result['entities']
            #for e in result['entities']['hashtags']:
                #print e['text']
            scraperwiki.sqlite.save(["id"], data) 

    except:
        break
        print 'Error with url: %s' % base_url
import scraperwiki
import time
import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice.
QUERY = 'http://www.guardian.co.uk/news/datablog/2012/sep/17/prison-probation-suicide-mapped'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
NUM_PAGES = 100

for page in range(1, NUM_PAGES+1):

    time.sleep(5)

    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&include_entities=true&page=%s'\
        % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    
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
            data['entities'] = result['entities']
            #for e in result['entities']['hashtags']:
                #print e['text']
            scraperwiki.sqlite.save(["id"], data) 

    except:
        break
        print 'Error with url: %s' % base_url
