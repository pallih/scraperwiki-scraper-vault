import scraperwiki
import simplejson
import urllib2

peer_handle = 'tijevlam'

base_url = 'http://api.peerreach.com/v1/multi-user/lookup.json?screen_name=' + peer_handle 

results_json = simplejson.loads(scraperwiki.scrape(base_url)

print results_json

