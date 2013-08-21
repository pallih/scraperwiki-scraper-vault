import scraperwiki
import json
import urllib2

source_name = "LisaTalia"
target_name = "roflson"

data = json.load(urllib2.urlopen('https://api.twitter.com/1/friendships/show.json?source_screen_name='+source_name+'&target_screen_name='+target_name))

print data
print data["relationship"]["target"]["id"]
print data["relationship"]["target"]["screen_name"]

