###############################################################################
# Twitter srcaper for the hashtag #Scrape10.
###############################################################################

import scraperwiki
import simplejson

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'American+Airlines'
options = '&rpp=100&page='

for page in range(1,2):
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            # save records to the datastore
            scraperwiki.sqlite.save(["id"], data) 
    except Exception as e:
        print e.message
        print str(page) + ' pages scraped'
        break
        
    