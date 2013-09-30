###################################################################################
# Esto es un comentario, acá puede ir cualquier cosa
###################################################################################

import scraperwiki
import simplejson
import urllib2

# QUERY es una VARIABLE que contiene un texto que define que la consulta que queremos hacer,
# acá se pueden introducir varios operadores como "from:nombre", que devuelve tweets enviados desde ese usuario
# más info de estos operadores acá: https://dev.twitter.com/docs/using-search
QUERY = 'from:deimidis'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'es'
NUM_PAGES = 10

for page in range(1, NUM_PAGES+1):

    # Esto es lo que se llama una búsqueda por GET, referencia en Twitter:
    # https://dev.twitter.com/docs/api/1/get/search
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&result_type=mixed&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['result_type'] = result['metadata']['result_type']
            
            rt_url = 'http://api.twitter.com/1/statuses/retweets/:%s.json' % (data['id'])
            #print rt_url
            rt_json = simplejson.loads(scraperwiki.scrape(rt_url))
            #print rt_json['retweeted_status']['retweet_count']

            if 'recent_retweets' in result['metadata']:
                data['retweets'] = result['metadata']['recent_retweets']
            else:
                data['retweets'] = 0

            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Uh, no se pudo escrapear %s' % base_url
        break
        
    ###################################################################################
# Esto es un comentario, acá puede ir cualquier cosa
###################################################################################

import scraperwiki
import simplejson
import urllib2

# QUERY es una VARIABLE que contiene un texto que define que la consulta que queremos hacer,
# acá se pueden introducir varios operadores como "from:nombre", que devuelve tweets enviados desde ese usuario
# más info de estos operadores acá: https://dev.twitter.com/docs/using-search
QUERY = 'from:deimidis'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'es'
NUM_PAGES = 10

for page in range(1, NUM_PAGES+1):

    # Esto es lo que se llama una búsqueda por GET, referencia en Twitter:
    # https://dev.twitter.com/docs/api/1/get/search
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&result_type=mixed&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['result_type'] = result['metadata']['result_type']
            
            rt_url = 'http://api.twitter.com/1/statuses/retweets/:%s.json' % (data['id'])
            #print rt_url
            rt_json = simplejson.loads(scraperwiki.scrape(rt_url))
            #print rt_json['retweeted_status']['retweet_count']

            if 'recent_retweets' in result['metadata']:
                data['retweets'] = result['metadata']['recent_retweets']
            else:
                data['retweets'] = 0

            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Uh, no se pudo escrapear %s' % base_url
        break
        
    