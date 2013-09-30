###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ("HealthCare", "Quality")]
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
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
                ttags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['tags']='::'.join(ttags)
                print data['from_user'], data['text']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break
###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import re

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ("HealthCare", "Quality")]
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
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
                ttags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['tags']='::'.join(ttags)
                print data['from_user'], data['text']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break
