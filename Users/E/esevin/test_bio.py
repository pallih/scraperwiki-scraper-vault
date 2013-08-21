import scraperwiki
import simplejson
import urllib2
import sys

SCREENNAME = 'indignezvousbe, damonmacwilson, anjumkiani, blockupy, drmerajs, occupywallst, colleenkelly, risingtidena, andersfoghr, chicagonato, nato, newsbalkan, usnato, socialnewscorp'

url = 'http://api.twitter.com/1/users/lookup.json?screen_name=%s' \
         % (urllib2.quote(SCREENNAME))

print 'getting url:', url

details_json = simplejson.loads(scraperwiki.scrape(url))
          
for detail in details_json:
        data = {'screen_name': detail['screen_name'],'id': detail['id'],'location': detail['location'], 'bio': detail['description'], 'followers_count': detail['followers_count'], 'following': detail['following']}
        print "Found person", data
        scraperwiki.sqlite.save(unique_keys=['id'], data = data)

    
