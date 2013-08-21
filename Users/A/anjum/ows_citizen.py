###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
from datetime import datetime
import urllib2
import sys

# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'from:antisec_ OR from:maxberger OR from:henaasharaf OR from:pocworkinggroup OR from:flyingmonkeyair OR from:anonyops OR from:gregmitch OR from:LukeRudkowski OR from:RebelDiaz OR from:owsoutreach OR from:allisonkilkenny OR from:lucykafanov OR from:JAMyerson  OR from:NaomiAKlein OR from:rdevro OR from:globalrevlive OR from:occupyinfo OR from:occupyarrests OR from:anonops OR from:occupythehood OR from:nyc_ga OR from:occupywallst OR from:Catherina_Guate AND since:2011-10-29 AND occupy OR ows'
RESULTS_PER_PAGE = '100'
LANGUAGE = 'en'
NUM_PAGES = 50

for page in range(1, NUM_PAGES+1):
    
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            data = {}
            data['date_scraped'] = datetime.now()
            data['created_at'] =  result['created_at']
            data['from_user'] = result['from_user'] + ' on ' + result['created_at']
            data['id'] = result['id']
            data['text'] = result['text']
            data['url'] = 'http://twitter.com/' + result['from_user']
            print data['date_scraped'], data['created_at'], data['from_user'], data['text'], data['id'], data['url']
            scraperwiki.sqlite.save(["id"], data)
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        

