###################################################################################
# Esto es un comentario, acá puede ir cualquier cosa
###################################################################################

import scraperwiki
import simplejson
import urllib2

# QUERY es una VARIABLE que contiene un texto que define la consulta que queremos hacer,
# acá se pueden introducir varios operadores como "from:nombre", que devuelve tweets enviados desde ese usuario
# más info de estos operadores acá: https://dev.twitter.com/docs/using-search
QUERY = '#8N'
RESULTS_PER_PAGE = 100
LANGUAGE = 'es'
NUM_PAGES = 100 

for page in range(1, NUM_PAGES+1):

    # Esto es lo que se llama una búsqueda por GET, referencia en Twitter:
    # https://dev.twitter.com/docs/api/1/get/search
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
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
            print data['from_user'], data['text']
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

# QUERY es una VARIABLE que contiene un texto que define la consulta que queremos hacer,
# acá se pueden introducir varios operadores como "from:nombre", que devuelve tweets enviados desde ese usuario
# más info de estos operadores acá: https://dev.twitter.com/docs/using-search
QUERY = '#aptoparacuriosos'
RESULTS_PER_PAGE = 100
LANGUAGE = 'es'
NUM_PAGES = 100 

for page in range(1, NUM_PAGES+1):

    # Esto es lo que se llama una búsqueda por GET, referencia en Twitter:
    # https://dev.twitter.com/docs/api/1/get/search
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
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
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Uh, no se pudo escrapear %s' % base_url
        break
        
    