import twitter
import json,operator

searchApi = twitter.Twitter(domain="search.twitter.com")
query = "#chess"
tweeters = dict()


for i in range(1,16):
    response = searchApi.search(q=query, rpp=100, page=i)
    tweets = response['results']
    for item in tweets:
        tweet = json.loads(json.dumps(item))
        user = tweet['from_user_name']
        print user
        if user in tweeters:
            print "list already contains", user
            tweeters[user] += 1 
        else:
            tweeters[user] = 1 
            
print len(tweeters)
sorted_tweeters = sorted(tweeters.iteritems(), key=operator.itemgetter(1),reverse=True)
print sorted_tweeters[0:10]    
print 'done'
    
