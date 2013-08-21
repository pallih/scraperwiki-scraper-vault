###################################################################################
# Twitter scraper - forked from Gartnersym, many thanks
###################################################################################

import scraperwiki
import simplejson
import urllib2
import time


Query_List=['fleg','flegs']

for q in Query_List:

    QUERY = q
    RESULTS_PER_PAGE = '100'
    LANGUAGE = 'all'
    NUM_PAGES = 1000 
    
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
             % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
        while True:
            try:
                results_json = simplejson.loads(scraperwiki.scrape(base_url))
                for result in results_json['results']:
                    #print result
                    data = {}
                    data['tweet_id'] = result['id']
                    data['query']=q
                    data['tweet_text'] = result['text']
                    data['tweet_from_user'] = result['from_user']
                    data['tweet_from_user_name']=result['from_user_name']
                    data['tweet_to_user'] = result['to_user']
                    data['tweet_to_user_name']=result['to_user_name']
                    data['tweet_created_at'] = result['created_at']
                    data['geo']=result['geo']
                    #print data['from_user'], data['text']
                    scraperwiki.sqlite.save(["id"], data) 
            except urllib2.HTTPError,e:
                if e.code==420:
                    print "Feed limit."
            except Exception,e:
                    print 'FAILED to scrape: %s' % base_url
                    print "Error: ",e
                    print "Query: ",q
                    print "Page: ",page
                    continue
            
    