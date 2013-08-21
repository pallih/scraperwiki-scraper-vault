import scraperwiki

# Blank Python

import sys
import tweepy

consumer_key="r3BvUpxEw5jpqW4kwmJwTA"
consumer_secret="2iLacbgJYo5T7E9KEUvXgEszD3OFdrGa1Tq5PWOLA4"
access_key = "37474406-9wbqqEs7FE3lLrc7xDv7cI13z6YFJvR4Brj9Vg8qg"
access_secret = "bIcvK91y7V2roxQP80kgrltOmZRbxP5Z4p9z0noD6Y" 


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=['-122.75,36.8,-121.75,37.8'])
