import scraperwiki

# Blank Python

#!/usr/bin/python

import urllib2
import simplejson

url = "http://text-processing.com/api/sentiment/"
sentence = "@chriswasser"

query = "text=%s" % sentence

request = urllib2.Request(url, query, {'Content-Type': 'application/json'})
response = urllib2.urlopen(request)
body = response.read()
sentiment = simplejson.loads(body)
print "Positive: %.2f%%" % sentiment['probability']['pos']
print " Neutral: %.2f%%" % sentiment['probability']['neutral']
print "Negative: %.2f%%" % sentiment['probability']['neg']