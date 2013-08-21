import scraperwiki
import simplejson

# retrieve a page
# base_url = 'http://search.twitter.com/search.json?q='
# q = '@mittromney'
# options = '&rpp=100&page='
# page = 1

# try a different query
base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name='
screen_name = 'twitterapi'
options = '&count=2'
page = 1


while 1:
    try:
#        url = base_url + screen_name + options + str(page)

        url = base_url + screen_name + options
        print url        
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
    except:
        print str(page) + ' pages scraped'
        break# Blank Python