import scraperwiki
import simplejson
import sys
import BeautifulSoup

# retrieve a page
base_url = 'https://twitter.com/cbSocially/social-fabric-community-2'
q= '/members'
page = 4

while 1:
    try:
        url = base_url + q
        html = scraperwiki.scrape(url)
        soup = simplejson.loads(html)
        for result in soup['results']:
            # save records to the datastore
            print "username"
            #scraperwiki.sqlite.save(["username"],result)
            # scraperwiki.sqlite.save(unique_keys=["id"], data={"a":1, "bbb":"Hi there"})
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Python