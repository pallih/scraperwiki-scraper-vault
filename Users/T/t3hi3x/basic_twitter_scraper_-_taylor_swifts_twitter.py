###################################################################################
# Facebook Page scraper - scrapes posts from a facebook page
###################################################################################

import scraperwiki
import simplejson
import urllib2

PAGE = 'IFeakingLoveScience'
RESULTS_PER_PAGE = '394' #394 is the max apparently
ACCESS_TOKEN = 'CAAE2y6xuPu8BAPlvluqK3tekZCvc8OYx52wf6TWosicL2fZB3eZBIBykiD0FktQVIZALQxoBy9t4xE7IW63y4wzo3j5fwZAucEgO0ah8AEd67kT0GFy2VKF8tnyZCrxWt7lvIRYVKnb0Qd7DdaRJNOzoDDd5cg4piZB7IbZBYmZBQ6wZDZD'
NUM_PAGES = 1 

for page in range(1, NUM_PAGES+1):
    base_url = 'https://graph.facebook.com/%s/feed/?access_token=%s&limit=%s' \
         % (PAGE, ACCESS_TOKEN, RESULTS_PER_PAGE)
    #try:
    results_json = simplejson.loads(scraperwiki.scrape(base_url))
    added = 0
    for result in results_json['data']:
        data = {}
        data['id'] = result['id']
        data['fron_id'] = result['from']['id']
        data['from_name'] = result['from']['name']
        #data['story'] = result['story']
        #data['picture'] = result['picture']
        data['type'] = result['type']
        data['created_time'] = result['created_time']
        #data['shares'] = result['shares']['count']
        #data['likes'] =  result['likes']['count']
        scraperwiki.sqlite.save(["id"], data)
        added = added + 1
    print 'Added %s' % added
    #except:
        #print 'Oh dear, failed to scrape %s' % base_url
        
    