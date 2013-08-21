# -*- coding: utf-8 -*-
import scraperwiki
import lxml.html
import time
import datetime
import tweepy
import cgi
import os
from random import choice
import string

chars = string.letters + string.digits
random =  ''.join([choice(chars) for i in xrange(4)]) # create a random string for url appending to avoid cache

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

#print qsenv

def sendtweet(msg):
    print 'Tweeting: %s' % msg
    try:
        auth = tweepy.OAuthHandler(qsenv["CONSUMER_KEY"], qsenv["CONSUMER_SECRET"])  
        auth.set_access_token(qsenv["ACCESS_KEY"], qsenv["ACCESS_SECRET"])
        api = tweepy.API(auth)
        api.update_status(msg)
        return True
    except Exception, e:
        print 'Failed to send tweet: %s' % msg
        print e
        return False

url = 'http://landspitali.is?x=' + random

html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
space = ' '
strings = root.xpath('//div[@class="activityNumbers activityNumbersNew"]')
# //div[@style="display: none;"]
for s in strings:
    record = {}
    messages = []
    for d in s[1:]:
        record['ward'] =  d.attrib['class']
        record['time'] = d[0].text
        record['number'] = d[1].text
        record['tail'] = d[2].text
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
#        for x in d.xpath('/div'):
#            print '    ', x[0].text, ' - ', x[1].text, x[2].text
        msg = record['time'].replace('...',':') + space + record['number'] +space + record['tail']
        messages.append(msg)
        print msg

#sendtweet(choice(messages))
#sendtweet(messages[2])
