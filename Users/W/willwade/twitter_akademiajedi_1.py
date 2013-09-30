import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'ashfordvineyard'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        soup = simplejson.loads(html)
        for result in soup['results'][0]:
            # save records to the datastore
            dog = simplejson.loads(result)
            print type(dog)

            
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Pythonimport scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'ashfordvineyard'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        soup = simplejson.loads(html)
        for result in soup['results'][0]:
            # save records to the datastore
            dog = simplejson.loads(result)
            print type(dog)

            
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Python