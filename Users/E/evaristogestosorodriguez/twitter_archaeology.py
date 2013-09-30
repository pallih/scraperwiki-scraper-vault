import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'https://twitter.com/search?q='
q = 'archaeology'
# options = ''
page = 1

while 1:
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
        break# Blank Python

import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'https://twitter.com/search?q='
q = 'archaeology'
# options = ''
page = 1

while 1:
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
        break# Blank Python

