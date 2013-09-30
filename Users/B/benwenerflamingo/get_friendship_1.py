import scraperwiki
import json
import urllib2
import sys

source_name = "M_A_D_Z"
target_name = "MishGov"

data = json.load(urllib2.urlopen('https://api.twitter.com/1/friendships/show.json?source_screen_name='+source_name+'&target_screen_name='+target_name))

print data
print data["relationship"]["target"]["id"]
print data["relationship"]["target"]["screen_name"]



import scraperwiki
import json
import urllib2
import sys

source_name = "M_A_D_Z"
target_name = "MishGov"

data = json.load(urllib2.urlopen('https://api.twitter.com/1/friendships/show.json?source_screen_name='+source_name+'&target_screen_name='+target_name))

print data
print data["relationship"]["target"]["id"]
print data["relationship"]["target"]["screen_name"]



