import scraperwiki
import simplejson
import urllib2

def search(queries = [],city = ['New York', '40.71,-74,50000m'], results_per_page = '100', language = 'en', num_pages = 15, geocode = None ):
    '''
    Get results from the Twitter API! Change QUERY to your search term of choice.
    Example queries: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
    '''
    for query in queries:
        for page in range(1, num_pages + 1):
            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&geocode=%s' \
                 % (urllib2.quote(query), results_per_page, language, page, city[1])
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                #print results_json
                for result in results_json['results']:
                    data = {}
                    data['id'] = result['id']
                    data['text'] = result['text']
                    data['from_user'] = result['from_user']
                    data['geo'] = result['geo']
                    data['city'] = city[0]
                    #print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data)
            except:
                print 'Oh dear, failed to scrape %s' % base_url
                raise    

#['buenos aires', '-34.5875,-58.6725,50km'],
# ['New York', '40.71,-74,50km']
CITIES = [ ['Buenos Aires', '-34.5875,-58.6725,50km'], ]
for city in CITIES:
    search(['bici','bike','bicicleta'], city = city)