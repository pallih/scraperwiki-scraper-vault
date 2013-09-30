import time
import scraperwiki
import simplejson
import sys

# config
hashtags = ['%22wiki%20loves%20monuments%22', 'wikilovesmonuments', '%23wlmpop', 'wikimonuments']
base_url = 'http://search.twitter.com/search.json?q='
q = '%20OR%20'.join(hashtags)
options = '&rpp=100&page=' # rpp = results per page
page = 1
totalpages = 100

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
        time.sleep(5)
    except:
        print str(page) + ' pages scraped'
        breakimport time
import scraperwiki
import simplejson
import sys

# config
hashtags = ['%22wiki%20loves%20monuments%22', 'wikilovesmonuments', '%23wlmpop', 'wikimonuments']
base_url = 'http://search.twitter.com/search.json?q='
q = '%20OR%20'.join(hashtags)
options = '&rpp=100&page=' # rpp = results per page
page = 1
totalpages = 100

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
        time.sleep(5)
    except:
        print str(page) + ' pages scraped'
        break