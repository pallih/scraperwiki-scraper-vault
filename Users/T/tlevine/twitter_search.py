import scraperwiki
import simplejson
import urllib2

def search(queries = [], results_per_page = '100', language = 'en', num_pages = 15 ):
    '''
    Get results from the Twitter API! Change QUERY to your search term of choice. 
    Example queries: 'newsnight', '#newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
    '''
    for query in queries:
        for page in range(1, num_pages + 1):
            base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
                 % (urllib2.quote(query), results_per_page, language, page)
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                for result in results_json['results']:
                    data = {}
                    data['id'] = result['id']
                    data['text'] = result['text']
                    data['from_user'] = result['from_user']
                    print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data) 
            except:
                print 'Oh dear, failed to scrape %s' % base_url
                raise    