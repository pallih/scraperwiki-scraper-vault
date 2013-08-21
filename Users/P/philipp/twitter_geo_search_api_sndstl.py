import scraperwiki
import simplejson
import sys
import tweepy
# retrieve a page
U = 'casy'
P = ''
q = '-122.75,36.8,-121.75,37.8'
base_url = 'https://stream.twitter.com/1.1/statuses/filter.json?locations=' + q + '- u' + U + ':' + P

       

page = 1

while 1:
    try:
        url = base_url
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

