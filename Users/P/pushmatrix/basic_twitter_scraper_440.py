###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
QUERY = '#datagatheroku'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 1 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&include_entities=true' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            if(result['geo']):
              if('entities' in result):
                if ('media' in result['entities']):
                    if(len(result['entities']['media']) > 0):
                      data = {}
                      data['id'] = result['id']
                      data['from_user'] = result['from_user']
                      data['created_at'] = result['created_at']
                      data['lat'] = result['geo']['coordinates'][0]
                      data['lng'] = result['geo']['coordinates'][1]
                      data['image'] = result['entities']['media'][0]['media_url']
                      print data['from_user']
                      scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break