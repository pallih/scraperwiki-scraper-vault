import scraperwiki
import simplejson

# retrieve a page
base_url = 'http://64.95.71.185:8080/Search.ashx?SearchKeywords=*&ClientKey=<yourAPIkey>&NumItems=
10&Sort=Date&ResultSet=Index&ResultType=Articles'
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
            # save records to the datastore
            scraperwiki.datastore.save(["id"], data)
        page = page + 1
    except:
        print str(page) + ' pages scraped'
        break

