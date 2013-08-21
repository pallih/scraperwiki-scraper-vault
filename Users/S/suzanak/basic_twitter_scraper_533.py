import scraperwiki
import simplejson
import urllib2
import urllib

# Get results from the Twitter API! 

search_term = 'Europe'
geocode = '37.781157,-122.398720,25mi'
date = '2013-05-10'
language = 'en'

NUM_PAGES = 2
RESULTS_PER_PAGE = '10'

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
        
    