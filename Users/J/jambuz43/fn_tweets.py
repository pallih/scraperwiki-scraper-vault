import scraperwiki
import simplejson
import sys

# config
hashtags = ['ReplacetaglinewithFoke'] # the # sharp is added in the line below
hashtags = ['%23'+h for h in hashtags] # %23 = #
base_url = 'http://search.twitter.com/search.json?q='
q = '%20OR%20'.join(hashtags)
options = '&rpp=100&page=' # rpp = results per page
page = 1
totalpages = 1000

# loop scraper
while page < totalpages + 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            # save records to the datastore
            scraperwiki.sqlite.save(["id"], result)
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        breakimport scraperwiki
import simplejson
import sys

# config
hashtags = ['ReplacetaglinewithFoke'] # the # sharp is added in the line below
hashtags = ['%23'+h for h in hashtags] # %23 = #
base_url = 'http://search.twitter.com/search.json?q='
q = '%20OR%20'.join(hashtags)
options = '&rpp=100&page=' # rpp = results per page
page = 1
totalpages = 1000

# loop scraper
while page < totalpages + 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            # save records to the datastore
            scraperwiki.sqlite.save(["id"], result)
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break