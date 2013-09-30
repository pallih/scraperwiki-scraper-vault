###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################
#changed lang, took out &lang=%s and line LANGUAGE='en' and line urllib2.quote LANGUAGE (after RESULTS_PER_PAGE)

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'from:AlejandroFalla OR from:RMachadoTenis OR from:JuanIChela OR from:micallodra OR from:dani_gimeno OR from:GGarciaLopez OR from:ElGirald OR from:pereribamadrid OR from:charlyberlocq OR from:albertramos88 OR from:benoitpaire OR from:bojo_jovanovski OR from:paula_ormaechea OR from:TaMmyTaMarine OR from:@CarlaSuarezNava'
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
        
    ###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################
#changed lang, took out &lang=%s and line LANGUAGE='en' and line urllib2.quote LANGUAGE (after RESULTS_PER_PAGE)

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'from:AlejandroFalla OR from:RMachadoTenis OR from:JuanIChela OR from:micallodra OR from:dani_gimeno OR from:GGarciaLopez OR from:ElGirald OR from:pereribamadrid OR from:charlyberlocq OR from:albertramos88 OR from:benoitpaire OR from:bojo_jovanovski OR from:paula_ormaechea OR from:TaMmyTaMarine OR from:@CarlaSuarezNava'
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
        
    