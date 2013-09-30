from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key="r3BvUpxEw5jpqW4kwmJwTA"
consumer_secret="2iLacbgJYo5T7E9KEUvXgEszD3OFdrGa1Tq5PWOLA4"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="37474406-9wbqqEs7FE3lLrc7xDv7cI13z6YFJvR4Brj9Vg8qg"
access_token_secret="bIcvK91y7V2roxQP80kgrltOmZRbxP5Z4p9z0noD6Y"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status



if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)    
    stream.filter(track=['basketball'])

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret will be generated for you after
consumer_key="r3BvUpxEw5jpqW4kwmJwTA"
consumer_secret="2iLacbgJYo5T7E9KEUvXgEszD3OFdrGa1Tq5PWOLA4"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="37474406-9wbqqEs7FE3lLrc7xDv7cI13z6YFJvR4Brj9Vg8qg"
access_token_secret="bIcvK91y7V2roxQP80kgrltOmZRbxP5Z4p9z0noD6Y"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status



if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)    
    stream.filter(track=['basketball'])

