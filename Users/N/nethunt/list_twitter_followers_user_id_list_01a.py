import scraperwiki
import simplejson
import urllib2
import sys

x = -1 # number of id's on array
n = 0 # number of processed id's
d = 0 # rate limit

# fuction: check available rate limit 150 / hour {'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       #Get the remaining hits for the hour

wasted = rate_json['remaining_hits']
#Put target id's here on the 'lista'
lista = [309766282,66750755,437815068,43335873,315686570,260330882,110761559]

while x <len(lista):
    SCREENID = lista[x]
    print "Processing node %d of %d, ID number %d" % (x, len(lista), lista[x])
    wasted = wasted - 1
    n = n + 1
    x = x + 1
    url = 'http://api.twitter.com/1/followers/ids.json?user_id=%d' % (SCREENID)
#    print 'getting url:', url
    followers_json = simplejson.loads(scraperwiki.scrape(url))
    print followers_json 
    print followers_json['ids'] 
    for cells in followers_json:
        data = followers_json['ids']
        node = {'noodi': SCREENID} 
#        data = {'ids': cells['ids']}
    print "Only %d hits to waste" % (wasted)
#Tallennuksessa on epäselvää vielä
#    scraperwiki.sqlite.save(unique_keys=['noodi'], data = data)

#{'reset_time': 'Thu Apr 05 22:13:14 +0000 2012', 'remaining_hits': 0, 'hourly_limit': 150, 'reset_time_in_seconds': 1333663994}
rate_url = 'https://api.twitter.com/1/account/rate_limit_status.json'
rate_json = simplejson.loads(scraperwiki.scrape(rate_url))
print rate_json
print 'You have %s hits left. Reload time is at - %s -' % (rate_json['remaining_hits'], rate_json['reset_time'])       #Get the remaining hits for the hour
print "Persons processed:", n