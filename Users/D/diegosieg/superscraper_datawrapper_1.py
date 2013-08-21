###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ('neutralidade','rede')]
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15 

for (q,table) in QUERY:
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(q), RESULTS_PER_PAGE, LANGUAGE, page)
        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            print results_json
            if len(results_json['results'])==0: break
            for result in results_json['results']:
                #print result
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id'] = result['from_user_id']
                data['to_user'] = result['to_user']
                data['to_user_id'] = result['to_user_id']
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['source'] = result['source']
                data['profile_image_url'] = result['profile_image_url']
                data['iso_language_code'] = result['iso_language_code']
                 
                thashtags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['hashtags']='::'.join(thashtags)
                
                tuser=re.findall("@([a-z0-9]+)", result['text'], re.I)
                data['user identified']='::'.join(tuser)
                
                thashtags=re.findall("RT @([a-z0-9]+)", result['text'], re.I)
                data['retweets']='::'.join(thashtags)

                thashtags=re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", result['text'], re.I)
                data['links']='$$$'.join(thashtags)

                print data['from_user'], data['text'], data['iso_language_code'], data['source'], data['geo'], data['profile_image_url']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data) 
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break

    