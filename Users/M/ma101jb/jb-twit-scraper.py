import scraperwiki

# Blank Python

###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import sys
import csv

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '%22bisping%22%20OR%20%22dan%20hardy%22%20OR%20%22john%20hathaway%22%20OR%20%22ross%20pearson%22%20OR%20%22paul%20daley%22%20OR%20%22brad%20pickett%22%20OR%20%22terry%20etim%22%20-free%20-%40'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 20 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    import scraperwiki

# Blank Python

###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import sys
import csv

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = '%22bisping%22%20OR%20%22dan%20hardy%22%20OR%20%22john%20hathaway%22%20OR%20%22ross%20pearson%22%20OR%20%22paul%20daley%22%20OR%20%22brad%20pickett%22%20OR%20%22terry%20etim%22%20-free%20-%40'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 20 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            #print result
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
        
    