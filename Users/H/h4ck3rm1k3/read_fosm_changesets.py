import scraperwiki
import sys
import os
import feedparser

def getid():
    url = "http://identi.ca/api/statuses/friends_timeline/fosmchangesets.atom"
    d = feedparser.parse(url)
    for e in d.entries:
        print e

def gettw():
    url = "http://search.twitter.com/search.atom?q=fosm"
    d = feedparser.parse(url)
    for e in d.entries:
        print e

def gettwusr(name):
    url = "http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=%s" % name
    d = feedparser.parse(url)
    for e in d.entries:
        print e

def getblog():
    url = "http://osmopenlayers.blogspot.de//feeds/posts/default"
    d = feedparser.parse(url)
    for e in d.entries:
        print e
    

gettwusr("h4ck3rm1k3")
