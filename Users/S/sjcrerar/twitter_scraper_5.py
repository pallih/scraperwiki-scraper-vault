import scraperwiki
import simplejson
import urllib2
import lxml.html 

#html = scraperwiki.scrape('http://www.civicarts.com/')
# 
#print html   
#root = lxml.html.fromstring(html) 



# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'Regina'
QUERY2 = 'art'
RESULTS_PER_PAGE = '50'
LANGUAGE = 'en'
NUM_PAGES = 20
for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    root = lxml.html.fromstring(base_url)
    #print root
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        #print results_json
        for result in results_json['results']:
            if QUERY2 in result['text']:
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                #print data['from_user'], data['text']
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
import scraperwiki
import simplejson
import urllib2
import lxml.html 

#html = scraperwiki.scrape('http://www.civicarts.com/')
# 
#print html   
#root = lxml.html.fromstring(html) 



# Change QUERY to your search term of choice. 
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = 'Regina'
QUERY2 = 'art'
RESULTS_PER_PAGE = '50'
LANGUAGE = 'en'
NUM_PAGES = 20
for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, LANGUAGE, page)
    root = lxml.html.fromstring(base_url)
    #print root
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))
        #print results_json
        for result in results_json['results']:
            if QUERY2 in result['text']:
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                #print data['from_user'], data['text']
                scraperwiki.sqlite.save(["id"], data) 
    except:
        print 'Oh dear, failed to scrape %s' % base_url
