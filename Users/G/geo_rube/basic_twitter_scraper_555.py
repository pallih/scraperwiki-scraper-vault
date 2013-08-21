###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import scraperwiki
import simplejson
import urllib2

# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'

QUERY='Algeria%20OR%20Angola%20OR%20Benin%20OR%20Botswana%20OR%20Faso%20OR%20Burundi%20OR%20Cameroon%20OR%20Canary%20OR%20Verde%20OR%20Ceut%20OR%20Chad%20OR%20Comoros%20OR%20Congo%20OR%20Djibouti%20OR%20egypt%20OR%20Guinea%20OR%20Eritrea%20OR%20Ethiopia%20OR%20Gabon%20OR%20Gambia%20OR%20Ghana%20OR%20Guinea%20OR%20Bissau%20OR%20Kenya%20OR%20Lesotho%20OR%20Liberia%20OR%20Libya%20OR%20Madagascar%20OR%20Madeira%20OR%20Malawi%20OR%20Mali%20OR%20Mauritania%20OR%20Mauritius'#%20OR%20Mayotte'#%20OR%20Melilla'#%20OR%20Morocco'#%20OR%20Mozambique'%20OR%20Namibia%20OR%20Niger%20OR%20Nigeria%20OR%20Rwanda%20OR%20Helena%20OR%20Senegal%20OR%20Seychelles%20OR%20Leone%20OR%20Somalia%20OR%20Sudan%20OR%20Swaziland%20OR%20Tanzania%20OR%20Togo%20OR%20Tunisia%20OR%20Uganda%20OR%20Sahara%20OR%20Zambia%20OR%20Zimbabwe'
RESULTS_PER_PAGE = '1000'
LANGUAGE = 'en'
NUM_PAGES = 10000 

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
        
    