import scraperwiki
import simplejson
import urllib2
import sys

# This script fetches the ids of followers of list of ids
# 1: Replace 'lista' in line 13 w ur own array of Twitter usernames
# 2: Click 'Run', wait and copy data from "Data" tab
x = 0

#Put target nicks here on the 'lista'
lista = [224671891, 510337177, 403713993, 465877238, 12063202, 20608977, 609663, 508704595, 80104598, 252547221, 346794088, 456588046]
while x <len(lista):
    SCREENNAME = lista[x]
    x = x + 1
    url = 'http://api.twitter.com/1/followers/ids.json?&user_id=%d' % (lista[x])
    print 'getting url:', url
    details_json = simplejson.loads(scraperwiki.scrape(url))
    print details_json
       scraperwiki.sqlite.save(unique_keys=['id'], data = data)
