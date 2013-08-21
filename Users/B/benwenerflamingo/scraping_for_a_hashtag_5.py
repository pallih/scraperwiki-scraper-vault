import scraperwiki
import simplejson
import urllib2
import sys

# create our twitter access object 
api = tweepy.API()
# downloads the timeline 
timeline = api.search(”#malaincuba” + “since:2012-01-01″‘)
# iterate through each of the tweets, + print its contents 
for result in timeline: print result.text print result.iso_language_code

