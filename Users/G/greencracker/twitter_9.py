import scraperwiki

import urllib
import json
import sys



def search_twitter(query='gapol'):
    url = 'http://search.twitter.com/search.json?q=' + query
    response = urllib.urlopen(url).read()
    data = json.loads(response)
    return data['results']
    
def print_tweets(tweets):
    for tweet in tweets:
        print tweet['from_user'] + ': ' + tweet['text'] + '\n'
        
results = search_twitter()
print_tweets(results)

if __name__ == "__main__":
    print "line 21 check"
    query = sys.argv[1]
    print "line 23 check"
    results = search_twitter(query)
    print "line 25 check"
    print_tweets(results)
print type(results[1].items())
print results[0].items()
print results[1].items()
print results[2].items()  

for result in results:
    print result.items()
    data = {
       'tweet_text' : result.items(),
                    
       }
#        print data
                
    scraperwiki.sqlite.save(unique_keys=['tweet_text'], data=data)
