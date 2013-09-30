import scraperwiki
import simplejson

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'driven%20OR%20drove%20OR%20drive%20OR%20driving%20OR%20lessons%20OR%20tuition%20OR%20adi'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at']= result['created_at']   


            # save records to the datastore
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        breakimport scraperwiki
import simplejson

# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
q = 'driven%20OR%20drove%20OR%20drive%20OR%20driving%20OR%20lessons%20OR%20tuition%20OR%20adi'
options = '&rpp=100&page='
page = 1

while 1:
    try:
        url = base_url + q + options + str(page)
        html = scraperwiki.scrape(url)
        #print html
        soup = simplejson.loads(html)
        for result in soup['results']:
            data = {}
            data['id'] = result['id']
            data['text'] = result['text']
            data['from_user'] = result['from_user']
            data['created_at']= result['created_at']   


            # save records to the datastore
            scraperwiki.sqlite.save(["id"], data) 
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break