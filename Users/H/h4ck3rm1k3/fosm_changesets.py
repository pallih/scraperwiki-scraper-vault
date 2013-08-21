import scraperwiki
import sys
import tweepy
DIR_LANGUAGE = None
import locale
locale.setlocale(locale.LC_ALL, DIR_LANGUAGE)

CONSUMER_KEY = '855a7483d853e6555e1cbd9c6572858d'
CONSUMER_SECRET = 'd973254012bbad772789d5a5b2cccadb'
ACCESS_KEY = 'b9258d54ae274a210ba5b7822de554f1'
ACCESS_SECRET = 'f00c737622578d0e8a740ab1bc61b16d'

post = "I microblog from scraperwikie"
host = 'identi.ca'
api_root = '/api/'
oauth_root = api_root + 'oauth/'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, 'oob')
auth.OAUTH_HOST = host 
auth.OAUTH_ROOT = oauth_root 
auth.secure = True 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, host = host, api_root = api_root)
api.update_status(post)