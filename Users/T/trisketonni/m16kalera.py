import scraperwiki

import simplejson
import urllib2
import re

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '#m16kalera'
RESULTS_PER_PAGE = '90000'
LANGUAGE = 'en'
NUM_PAGES = 10

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            mentions = re.findall(r'@(\w+)', result['text'])
            i = 0
            for mention in mentions:
                data = {}
                data['id'] = result['id']+i
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['created_at'] = result['created_at']
                data['to_user'] = mention
                scraperwiki.sqlite.save(['id'], data) 
                i += 1
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break