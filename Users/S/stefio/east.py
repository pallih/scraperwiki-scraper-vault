import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.east.co.uk/page/storedetail/?sid='

record = {}

for i in range(1,150):
    html = scraperwiki.scrape(starting_url + str(i))
    print html
    soup = BeautifulSoup(html)
    stores =soup.find("li", { "class" : "fs-small" })
    if not (stores is None):
        stores = stores.prettify().split('<br />')
        for store in stores:
            print store
            if (store[-4:-2]=='li'):
                record['id'] = i
                record['postcode'] = store[:-6]
                scraperwiki.sqlite.save(['id'], record)import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.east.co.uk/page/storedetail/?sid='

record = {}

for i in range(1,150):
    html = scraperwiki.scrape(starting_url + str(i))
    print html
    soup = BeautifulSoup(html)
    stores =soup.find("li", { "class" : "fs-small" })
    if not (stores is None):
        stores = stores.prettify().split('<br />')
        for store in stores:
            print store
            if (store[-4:-2]=='li'):
                record['id'] = i
                record['postcode'] = store[:-6]
                scraperwiki.sqlite.save(['id'], record)