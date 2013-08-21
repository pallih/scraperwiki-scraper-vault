import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'https://twitter.com/DeniseBerger11/journalisten-project-x'
q= '/members'
page = 1000

while 1:
    try:
        url = base_url + q
        html = scraperwiki.scrape(url)
        soup = simplejson.loads(html)
        for result in soup['results']:
            # save records to the datastore
            scraperwiki.sqlite.save(["id"], result)
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break# Blank Python