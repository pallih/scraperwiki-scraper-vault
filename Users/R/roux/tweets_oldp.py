import scraperwiki
import simplejson
import re
     
# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
options = '&rpp=100&page='
     
def scrape_query(q):
    page = 1
    while 1:
        try:
            url = base_url + q + options + str(page)
            html = scraperwiki.scrape(url)
            #print html
            soup = simplejson.loads(html)
            for result in soup['results']:
                #print result['text']
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']        
                data['from_user'] = result['from_user']
                data['created_at'] = result['created_at']
                data['twitter_url'] = 'https://twitter.com/'+data['from_user']+'/statuses/'+`result['id']`
                data['photo_user'] = 'http://twitteravatar.appspot.com/users/avatar/'+data['from_user']
                if result['geo'] is not None:
                    data['geoloc'] = result['geo']['coordinates']
                # save records to the datastore
                scraperwiki.sqlite.save(["id"], data)
            page = page + 1
        except:
            print str(page) + ' pages scraped'
            break# Blank Python

scrape_query('%23OLDP+OR+%28Open+legislative+data%29+OR+%28OpenData+legislative%29+OR+%22La+Fabrique+de+la+Loi%22+OR+lafabriquedelaloi')
import scraperwiki
import simplejson
import re
     
# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
options = '&rpp=100&page='
     
def scrape_query(q):
    page = 1
    while 1:
        try:
            url = base_url + q + options + str(page)
            html = scraperwiki.scrape(url)
            #print html
            soup = simplejson.loads(html)
            for result in soup['results']:
                #print result['text']
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']        
                data['from_user'] = result['from_user']
                data['created_at'] = result['created_at']
                data['twitter_url'] = 'https://twitter.com/'+data['from_user']+'/statuses/'+`result['id']`
                data['photo_user'] = 'http://twitteravatar.appspot.com/users/avatar/'+data['from_user']
                if result['geo'] is not None:
                    data['geoloc'] = result['geo']['coordinates']
                # save records to the datastore
                scraperwiki.sqlite.save(["id"], data)
            page = page + 1
        except:
            print str(page) + ' pages scraped'
            break# Blank Python

scrape_query('%23OLDP+OR+%28Open+legislative+data%29+OR+%28OpenData+legislative%29+OR+%22La+Fabrique+de+la+Loi%22+OR+lafabriquedelaloi')
