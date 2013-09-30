###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import urlparse
import dateutil.parser
import requests

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'multiple sclerosis'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
auth = ('scraperwiki_bot','pondsimplestevernumber')
page = 1
base_url='http://api.supertweet.net/1/search.json?q=%s&rpp=%s&lang=%s' \
          % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE)
        
def twitter_to_sql(url, table='sw_data', next_page=True):
    try:
        print url
        results_raw=requests.get(base_url, auth=auth)
        results_json = simplejson.loads(results_raw.content)
        builder=[]
        results= results_json['results']
        scraperwiki.sqlite.save(table_name=table, data=results, unique_keys=['id'])
        print results_raw.content
        print len(results)
        if 'next_page' in results_json and next_page:
            newurl=urlparse.urljoin(url,results_json['next_page'],next_page)
            twitter_to_sql(newurl, table)

    except:
        print 'Oh dear, failed to scrape %s' % base_url
        print results_raw
        print results_raw.content
        
        

#twitter_to_sql(base_url)

users=[x['id'] for x in scraperwiki.sqlite.select('distinct from_user_id_str as id from sw_data')]
for user in users:
    url='http://api.supertweet.net/1/users/show.json?screen_name=%s&include_entities=true'%user
    twitter_to_sql(url, 'users', False)
        ###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import urlparse
import dateutil.parser
import requests

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'multiple sclerosis'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
auth = ('scraperwiki_bot','pondsimplestevernumber')
page = 1
base_url='http://api.supertweet.net/1/search.json?q=%s&rpp=%s&lang=%s' \
          % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE)
        
def twitter_to_sql(url, table='sw_data', next_page=True):
    try:
        print url
        results_raw=requests.get(base_url, auth=auth)
        results_json = simplejson.loads(results_raw.content)
        builder=[]
        results= results_json['results']
        scraperwiki.sqlite.save(table_name=table, data=results, unique_keys=['id'])
        print results_raw.content
        print len(results)
        if 'next_page' in results_json and next_page:
            newurl=urlparse.urljoin(url,results_json['next_page'],next_page)
            twitter_to_sql(newurl, table)

    except:
        print 'Oh dear, failed to scrape %s' % base_url
        print results_raw
        print results_raw.content
        
        

#twitter_to_sql(base_url)

users=[x['id'] for x in scraperwiki.sqlite.select('distinct from_user_id_str as id from sw_data')]
for user in users:
    url='http://api.supertweet.net/1/users/show.json?screen_name=%s&include_entities=true'%user
    twitter_to_sql(url, 'users', False)
        