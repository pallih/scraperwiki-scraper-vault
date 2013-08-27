###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

#import traceback
import scraperwiki
import simplejson
import urllib2


QUERY = ['#14N','#14Nov','#14Nov2012', '#GENERALSTRIKE','#14NRiseUP', '#GreveGeral', '#HuelgaGeneral', '#VagaGeneral', '#grèvegénérale']
LANGUAGES= ['es','pt','it','en','fr','el','de','ga','eu','fi','da']
RESULTS_PER_PAGE = '100'
NUM_PAGES = 1000
for l in LANGUAGES:
    for q in QUERY:
        for page in range(1, NUM_PAGES+1):
            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&include_entities=true&result_type=mixed' \
                 % (urllib2.quote(q), RESULTS_PER_PAGE, l, page)
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                for result in results_json['results']:
                    #print result
                    data = {}
                    data['query'] = q
                    data['entities'] = result["entities"]
                    data['id'] = result['id']
                    data['text'] = result['text']
                    data['from_user'] = result['from_user']
                    data['created_at'] = result['created_at']
                    data['geo'] = result['geo']
                    data['language'] = l
                    print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data) 
            except Exception, e:
                print 'Oh dear, failed to scrape %s' % base_url
                #traceback.print_exc()
                continue    
###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

#import traceback
import scraperwiki
import simplejson
import urllib2


QUERY = ['#14N','#14Nov','#14Nov2012', '#GENERALSTRIKE','#14NRiseUP', '#GreveGeral', '#HuelgaGeneral', '#VagaGeneral', '#grèvegénérale']
LANGUAGES= ['es','pt','it','en','fr','el','de','ga','eu','fi','da']
RESULTS_PER_PAGE = '100'
NUM_PAGES = 1000
for l in LANGUAGES:
    for q in QUERY:
        for page in range(1, NUM_PAGES+1):
            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&include_entities=true&result_type=mixed' \
                 % (urllib2.quote(q), RESULTS_PER_PAGE, l, page)
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                for result in results_json['results']:
                    #print result
                    data = {}
                    data['query'] = q
                    data['entities'] = result["entities"]
                    data['id'] = result['id']
                    data['text'] = result['text']
                    data['from_user'] = result['from_user']
                    data['created_at'] = result['created_at']
                    data['geo'] = result['geo']
                    data['language'] = l
                    print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data) 
            except Exception, e:
                print 'Oh dear, failed to scrape %s' % base_url
                #traceback.print_exc()
                continue    
###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

#import traceback
import scraperwiki
import simplejson
import urllib2


QUERY = ['#14N','#14Nov','#14Nov2012', '#GENERALSTRIKE','#14NRiseUP', '#GreveGeral', '#HuelgaGeneral', '#VagaGeneral', '#grèvegénérale']
LANGUAGES= ['es','pt','it','en','fr','el','de','ga','eu','fi','da']
RESULTS_PER_PAGE = '100'
NUM_PAGES = 1000
for l in LANGUAGES:
    for q in QUERY:
        for page in range(1, NUM_PAGES+1):
            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&include_entities=true&result_type=mixed' \
                 % (urllib2.quote(q), RESULTS_PER_PAGE, l, page)
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                for result in results_json['results']:
                    #print result
                    data = {}
                    data['query'] = q
                    data['entities'] = result["entities"]
                    data['id'] = result['id']
                    data['text'] = result['text']
                    data['from_user'] = result['from_user']
                    data['created_at'] = result['created_at']
                    data['geo'] = result['geo']
                    data['language'] = l
                    print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data) 
            except Exception, e:
                print 'Oh dear, failed to scrape %s' % base_url
                #traceback.print_exc()
                continue    
