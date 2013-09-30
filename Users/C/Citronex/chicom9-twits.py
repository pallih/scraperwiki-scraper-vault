import scraperwiki

# Blank Python
import urllib
import simplejson

def searchTweets(query):
 search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
 dict = simplejson.loads(search.read())
 for result in dict["results"]: # result is a list of dictionaries
           data = {}
           data['id'] = result['id']
           data['text'] = result['text']
           data['from_user'] = result['from_user']
           data['created_at'] = result['created_at']
           print data['from_user'], data['text'], data['from_user'], data['created_at']

#print "*",result["text"],"\n"

# we will search tweets about "anything ont the searchtweets function"
searchTweets("Crime+Mexico&rpp=20")


import scraperwiki

# Blank Python
import urllib
import simplejson

def searchTweets(query):
 search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
 dict = simplejson.loads(search.read())
 for result in dict["results"]: # result is a list of dictionaries
           data = {}
           data['id'] = result['id']
           data['text'] = result['text']
           data['from_user'] = result['from_user']
           data['created_at'] = result['created_at']
           print data['from_user'], data['text'], data['from_user'], data['created_at']

#print "*",result["text"],"\n"

# we will search tweets about "anything ont the searchtweets function"
searchTweets("Crime+Mexico&rpp=20")


