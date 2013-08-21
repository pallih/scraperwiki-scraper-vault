###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import dateutil.parser
import requests

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'scraperwiki'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
auth = ('scraperwiki_bot','pondsimplestevernumber')

page = 0
while True:
    page=page+1

    #base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
    #     % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    base_url='http://api.supertweet.net/1/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
          % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    
    try:
        results_raw=requests.get(base_url, auth=auth)
        #print results_raw
        results_json = simplejson.loads(results_raw.content)
        #print results_json
        builder=[]
        results=[]
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            data['nicedate'] = dateutil.parser.parse (result['created_at'])
            builder.append(data)
            results.append(result)
        scraperwiki.sqlite.save(["id"], data=builder) 
        scraperwiki.sqlite.save(table_name='raw', data=results, unique_keys=['id'])
        print len(builder)
        if 'next_page' not in results_json:
            break

    except:
        print 'Oh dear, failed to scrape %s' % base_url
        print results_json
        raise
        break
        
    