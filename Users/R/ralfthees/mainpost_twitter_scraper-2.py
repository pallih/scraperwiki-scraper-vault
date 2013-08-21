###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'mainpost'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'de'
NUM_PAGES = 1000 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?include_entities=1&q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['mpid']=''
            data['url']=''
            if len(result['entities']['urls'])>0:
                m=result['entities']['urls'][0]['expanded_url']
                data['url']=m
                m = re.match(r'.*(http\:\/\/.*mainpost.de.*)[/,]([0-9]+).*', data['url']) #(http://t\.co(.*)\w+)
                if m:
                    data['mpid'] = m.group(2)
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    