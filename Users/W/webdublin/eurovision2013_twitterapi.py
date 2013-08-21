import sys
#import tweepy
#import scraperwiki
import time
import datetime
import cgi
import urllib
import os
import oauth2 as oauth

# this brings in the API keys for twitter 
qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
PAGES = 15

def Main():
    home_timeline = oauth_req(
      'https://api.twitter.com/1.1/search/tweets.json?q=%23eurovision',
      qsenv["CONSUMER_KEY"], 
      qsenv["CONSUMER_SECRET"]
    )
    #auth = tweepy.OAuthHandler(qsenv["CONSUMER_KEY"], qsenv["CONSUMER_SECRET"])  
    #auth.set_access_token(qsenv["ACCESS_KEY"], qsenv["ACCESS_SECRET"])
    #api = tweepy.API(auth)    
    #for p in range(1, PAGES):
    #    results = api.search(q='#eurovision', page=p, rpp = 100)
    #    time.sleep(5)
    #    for r in results:
    #        print r.text
        #print results


# need to establish whether there is a progression of SPUD Date, Date TD Reached, Completion Date
nowtime = datetime.date.today()

def daysago(ldate):
    ddate = datetime.datetime.strptime(ldate, "%Y-%m-%d").date()
    ddiff = nowtime - ddate
    if ddiff.days < 0:
        return "%d days in the future!!!" % (-ddiff.days)
    if ddiff.days == 0:
        return "today"
    if ddiff.days == 1:
        return "yesterday"
    if ddiff.days <= 60:
        return "%d days ago" % ddiff.days
    return "%.1f months ago" % (ddiff.days/30.0)


def GenerateTweet(rec, prevrecord):
    msg = "Twitter API 1.1 Test Tweet"   
    return msg


# using twitter account goatchurch
# north sea oil wells app:  

# https://dev.twitter.com/apps/1258499/show
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

def oauth_req(url, key, secret, http_method="GET", post_body=None,
        http_headers=None):
    consumer = oauth.Consumer(key=qsenv["CONSUMER_KEY"], secret=qsenv["CONSUMER_SECRET"])
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(
        url,
        method=http_method,
        body="",
        headers=http_headers
    )
    return content

Main()

