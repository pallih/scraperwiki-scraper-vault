import scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'http://civic.mit.edu/blog/pablo/3-steps-to-measure-the-corruption-coverage-in-spain'
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
        break# Blank Pythonimport scraperwiki
import simplejson
import sys

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'http://civic.mit.edu/blog/pablo/3-steps-to-measure-the-corruption-coverage-in-spain'
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