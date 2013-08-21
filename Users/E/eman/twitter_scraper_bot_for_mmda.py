import sys
import tweepy
import scraperwiki
import time

def a():
    scraperwiki.sqlite.attach("name of first scraper to be included")
    scraperwiki.sqlite.attach("name of second scraper to be included")

#This blog describes how to best use twitter OAuth http://talkfast.org/2010/05/31/twitter-from-the-command-line-in-python-using-oauth

CONSUMER_KEY = 'Put consumer key'
CONSUMER_SECRET = 'Put consumer secret'
ACCESS_KEY = 'Put access key here'
ACCESS_SECRET = 'Put access secret here'

def sendtweet(text):
    msg = text
    #Make sure tweets are 140 chars max
    if len(msg)>140:
        msg = text[:129]+"...#hashtag"
    print 'Tweeting: %s' % msg
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(msg)
    except Exception, e:
        print 'Failed to send tweet: %s' % msg
        print e
    time.sleep(10)


def test():
    # How many do we want each time?
    limit = 3

    # Get where we got to last time to be used as the offset
    x = scraperwiki.sqlite.get_var('last_item', 0)
    line_count = 0

    print 'Start - Setting offset to %s' % x

    #This SQL query calls the data and orders it form the scrapers attached, two examples given to show how I got different sentences

    for line in scraperwiki.sqlite.select(" * from (select `Date`, `Permanent Secretary` as `Person`, `Name of Organisation` as `From`,`Purpose of meeting` as `For`, 1 as `type` from permanent_secretaries_meetings_with_external_organ.swdata union select `Date of Hospitality`, `Minister`, `Name of Organisation`,`Type of hospitality received`, 2 from ministerial_hospitality_from_external_organisation.swdata) order by `Date` limit %s,%s" % (x,limit,) ):

        line_count = line_count + 1

        if line["type"] == 1:
            sendtweet ("On %s, %s met with %s about %s #Scrape10" % (line["Date"], line["Person"].split(",")[0].strip().replace("The","").replace(" Rt", "").replace(" Hon ", "").replace(" MP",""), line["From"], line["For"]))

        if line["type"] == 2:
            sendtweet ("On %s, %s got %s from %s #Scrape10" % (line["Date"], line["Person"].split(",")[-1].strip().replace("The","").replace(" Rt", "").replace(" Hon ", "").replace(" MP",""), line["For"], line["From"]))


        # Set the last one we processed to be used as the offset next time
        x = x + 1
        print 'Updating last processed to %s' % x
        scraperwiki.sqlite.save_var('last_item', x )


