import scraperwiki
import json
import urllib2
import sys

source_name = "zephoria"

data = json.load(urllib2.urlopen('https://api.twitter.com/1/friends/show.json?source_screen_name='+source_name+'&target_screen_name='+target_name'))


