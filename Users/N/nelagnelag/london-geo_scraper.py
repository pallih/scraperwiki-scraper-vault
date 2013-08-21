###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

#original author - paolop, modified by nelagnelag

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'


QUERY = ''
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 1000 

# lat, lon coordinates of city center
cityCenter = "51.5081289,-0.128005"
radius = 100  #radius in km
location = cityCenter + "," + str(radius) + "km"

for page in range(1, NUM_PAGES+1):

    base_url = 'http://search.twitter.com/search.json?geocode=' + location

    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        for result in results_json['results']:
            if result['geo']:
                #print result
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_name'] = result['from_user_name']
                data['created_at'] = result['created_at']
                data['to_user'] = result['to_user']
                data['geo'] = result['geo']            
                print data['from_user'], data['text']
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
        break
