import scraperwiki
import urllib2
import simplejson
import time

query = "#Obama"
pages = 0

for page in range(pages+1,pages+101):
    api_call = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s' % (urllib2.quote(query), 100, page)
    try:
        results_json = simplejson.loads(scraperwiki.scrape(api_call))
        for result in results_json['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at'] = result['created_at']
            scraperwiki.sqlite.save(["id"], data) 
    except:
        print "Error Page %s" % (page)
        time.sleep(10)
        continue
    time.sleep(5)