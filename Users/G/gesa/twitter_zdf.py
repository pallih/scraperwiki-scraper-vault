import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'zdfsport' or 'olympia' or 'olympische spiele' or 'Olympiade' or 'stream' or 'streaming' or 'kanal' or 'online' or 'Mediathek' or 'tv' or 'Sport1' or 'ard' or 'ebu' or 'seite' or 'site'
options = '&rpp=100&page='
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