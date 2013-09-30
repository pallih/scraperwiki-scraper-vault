###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import datetime

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'PCC "Police Commissioner"
QUERY = 'morano'
RESULTS_PER_PAGE = '500'
LANGUAGE = 'fr'
NUM_PAGES = 10 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        total = 0
   
        zetweettime_date_prec = datetime.datetime.now()
        #print zetweettime_date_prec

        for result in results_json['results']:
            total = total+1
            
            zetweettime = result['created_at']
            #print result['text'],result['created_at']
            zetweettime_date = datetime.datetime.strptime(zetweettime,"%a, %d %b %Y %H:%M:%S +0000")
            #print zetweettime_date
            if zetweettime_date.strftime("%d/%m/%Y") != zetweettime_date_prec.strftime("%d/%m/%Y"):
                data = {}
                data['id'] = zetweettime_date_prec.strftime("%d/%m/%Y")
                data['count'] = total
                scraperwiki.sqlite.save(["id"], data)
                total = 0
                zetweettime_date_prec = zetweettime_date
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    ###################################################################################
# Twitter API scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2
import datetime

# Get results from the Twitter API! Change QUERY to your search term of choice. 
# Examples: 'PCC "Police Commissioner"
QUERY = 'morano'
RESULTS_PER_PAGE = '500'
LANGUAGE = 'fr'
NUM_PAGES = 10 

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        total = 0
   
        zetweettime_date_prec = datetime.datetime.now()
        #print zetweettime_date_prec

        for result in results_json['results']:
            total = total+1
            
            zetweettime = result['created_at']
            #print result['text'],result['created_at']
            zetweettime_date = datetime.datetime.strptime(zetweettime,"%a, %d %b %Y %H:%M:%S +0000")
            #print zetweettime_date
            if zetweettime_date.strftime("%d/%m/%Y") != zetweettime_date_prec.strftime("%d/%m/%Y"):
                data = {}
                data['id'] = zetweettime_date_prec.strftime("%d/%m/%Y")
                data['count'] = total
                scraperwiki.sqlite.save(["id"], data)
                total = 0
                zetweettime_date_prec = zetweettime_date
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    