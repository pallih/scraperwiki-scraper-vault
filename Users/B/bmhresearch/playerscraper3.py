###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################
#changed lang, took out &lang=%s and line LANGUAGE='en' and line urllib2.quote LANGUAGE (after RESULTS_PER_PAGE)

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'from:Petzsche OR from:Annagroenefeld OR from:A_Pivovarova OR from:queen_v21 OR from:caseydellacqua OR from:jesselevine7 OR from:jojomelzer OR from:DevinBritton OR from:rebecca_marino OR from:dusanVemic OR from:EdinaGallovits OR from:arinarodionova OR from:melaniesouth OR from:k_skupski OR from:sarahborwell'
RESULTS_PER_PAGE = '100'
#LANGUAGE = 'en'
NUM_PAGES = 15

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['created_at']= result['created_at'] 
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            print data['from_user'], data['text']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        
    