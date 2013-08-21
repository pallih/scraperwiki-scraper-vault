import scraperwiki
import Twitter

# Blank Python

import json, operator, twitter
#construct twitter API object
searchApi = twitter.Twitter(domain="search.twitter.com")
#Get Trends
query = "#Doprah"
#start with an empty dictionary and put values in
tweeters=dict()


for i in range (1,16):
    response = searchApi.search(q=query, rpp=100, page=i)
    tweets = response ['results']
    for item in tweets:
        tweet = json.loads(json.dumps(item))
        user = tweet['from_user_name']
        if user in tweeters:
            tweeters[user] += 1
        else:
            tweeters [user] = 1
    
        
print len(tweeters)
sorted_tweeters = sorted(tweeters.iteritems(), key=operator.itemgetter(1),reverse=True)
print sorted_tweeters[0:10]
print 'done'