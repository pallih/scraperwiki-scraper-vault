import scraperwiki
import simplejson
import urllib2
import urllib

# Get results from the Twitter API! 

search_term = ''
# geocode = '37.5901463,-77.5563761,20mi'
# geocode = '13.097536,80.26577,100'
geocode = '51.5171,0.1062,20mi'
date = '2013-05-16'
language = 'en'

NUM_PAGES = 2
RESULTS_PER_PAGE = '100000'

basic_url = 'https://search.twitter.com/search.json?'
query_dict = {'q':search_term, 'lang':language, 'geocode':geocode, 'until':date}
query = urllib.urlencode(query_dict)

for page in range(1, NUM_PAGES+1):

        fh = urllib.urlopen(basic_url + query)
        response = fh.read()        
        result_json = simplejson.loads(response)
        # print result_json
        #print result_json['results']
        for result in result_json['results']:
            #print result
            result['geocode'] = geocode
            scraperwiki.sqlite.save(unique_keys=['id'], data=result, table_name="Tweets")
        
    

import scraperwiki
import simplejson
import urllib2
import urllib

# Get results from the Twitter API! 

search_term = ''
# geocode = '37.5901463,-77.5563761,20mi'
# geocode = '13.097536,80.26577,100'
geocode = '51.5171,0.1062,20mi'
date = '2013-05-16'
language = 'en'

NUM_PAGES = 2
RESULTS_PER_PAGE = '100000'

basic_url = 'https://search.twitter.com/search.json?'
query_dict = {'q':search_term, 'lang':language, 'geocode':geocode, 'until':date}
query = urllib.urlencode(query_dict)

for page in range(1, NUM_PAGES+1):

        fh = urllib.urlopen(basic_url + query)
        response = fh.read()        
        result_json = simplejson.loads(response)
        # print result_json
        #print result_json['results']
        for result in result_json['results']:
            #print result
            result['geocode'] = geocode
            scraperwiki.sqlite.save(unique_keys=['id'], data=result, table_name="Tweets")
        
    

