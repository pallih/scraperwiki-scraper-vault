import scraperwiki
import urllib2
import simplejson
import time
import tweepy
import collections
import networkx as nx
import math
from sets import Set
import matplotlib.pyplot as plt

#Does an OAuth login to access Twitter API using application settings
def OAuth():
    consumer_key = 'CS7ao75neMHDh8uTCJ3Nng'
    consumer_pass = '9xGJIWnjk7KRBi8Rw097KYlKd7sf2svwj9L6FpMIsA'

    access_key = '819221646-iaVneMz5ltxcC9osFmJ9v9D4W4PQBIbG4jZwAXXc'
    access_pass = '4h9VvHttlrWUqGcY8iQ7J0ZYDYCfbO0019BMhWNXkME'

    auth1 = tweepy.auth.OAuthHandler(consumer_key,consumer_pass)
    auth1.set_access_token(access_key,access_pass)

    api = tweepy.API(auth1)
    return api


#Gets tweets
def getTweets(api,celebrity):
    holder = []
    for pg in range(25):
        timeline = api.user_timeline(celebrity, page = pg)
        holder.extend(timeline)
        if len(timeline) == 0:
            break
    return holder

#Returns list of users whom the celebrity mentions in a particular tweet
def getMentions(api,celebrity,tweet):
    handles = collections.Counter()
    text = tweet.text
    text = text.split(" ")
    for part in text:
        if part.__contains__("@"):
            handles[part[1:]] += 1
    return handles

#Returns reply chains, if celebrity is talking to someone or group of people
def getResponses(api,celebrity,tweet):
    handles = collections.Counter()
    reply = tweet.in_reply_to_screen_name
    handles[reply] += 1
    del handles[None]
    return handles
     
#Collects mutual friends of a celebrity
def makeFriends(celebrity, responses, mentions):
    g = nx.Graph()
    mentionskeys = mentions.keys()
    responseskeys = responses.keys()
    for mentioned in mentionskeys:
        g.add_edge(celebrity,mentioned, weight = 1.0/mentions[mentioned], color = 'blue')

    for responded in responseskeys:
        g.add_edge(celebrity,responded, weight = 1.0/responses[responded], color = 'red')
    
    nx.draw(g)
    plt.show()
    return g

def drawInnerCircle(celebrity, responses, mentions):
    totals = collections.Counter()
    totals.update(responses)
    totals.update(mentions)
    size = len(totals.keys())
    topQuarter = size/4
    topQuarter = totals.most_common(topQuarter)
    topQuarter = topQuarter[-1][1]

    nodelistA = []
    nodelistB = []
    
    keys = totals.keys()
    for i in range(size):
        key = keys[i]
        weight = totals[key]
        if weight >= topQuarter:
            nodelistA.append(i)
        else:
            nodelistB.append(i)
        
    
    
    

def main():
    api = OAuth()

    handles = [
    "https://twitter.com/TheRealStanLee",
    "https://twitter.com/megatokyo",
    "https://twitter.com/NEBU_KURO",
    "https://twitter.com/masijacoke85",
    "https://twitter.com/travelchannel",
    "https://twitter.com/Bourdain",
    "https://twitter.com/ciaela",
    "https://twitter.com/petersgreenberg",
    "https://twitter.com/OJessicaNigri",
    "https://twitter.com/AlodiaAlmira",
    "https://twitter.com/ladygaga",
    "https://twitter.com/Oprah",
    "https://twitter.com/kevjumba",
    "https://twitter.com/Machinima_com",
    "https://twitter.com/coollike",
    "https://twitter.com/jfa_nadeshiko",
    "https://twitter.com/usainbolt",
    "https://twitter.com/GordonRamsay01",
    "https://twitter.com/EpicMealTime",
    "https://twitter.com/utadahikaru",
    "https://twitter.com/JayZ",
    "https://twitter.com/masason",
    "https://twitter.com/jack",
    "https://twitter.com/VictorQuest",
    "https://twitter.com/CarnegieMellon",
    "https://twitter.com/LuisvonAhn",
    "https://twitter.com/yun0808",
    "https://twitter.com/touya_skulldy",
    "https://twitter.com/siu3334"
    ]
    handles = [ handle[20:] for handle in handles]

    for celebrity in handles[23:24]:
        user = api.get_user(celebrity)
        timeline = getTweets(api,celebrity)
        print celebrity
        mentions = collections.Counter()
        responses = collections.Counter()
        for tweet in timeline:
            mentions.update(getMentions(api,celebrity,tweet))
            responses.update(getResponses(api,celebrity,tweet))
        print "Mentions", mentions
        print "Responses", responses

        #makeFriends(celebrity,responses,mentions)
        drawInnerCircle(celebrity,responses,mentions)
        '''
        intersection = {}
        conv = mentions.keys()
        for con in conv:
            value = mentions[con]*responses[con]
            value = math.sqrt(value)
            if value > 0:
                intersection[con] = value
        print "Intersection", intersection
        '''
            
            
main()

#'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'text', 'truncated', 'user'
# in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str'
import scraperwiki
import urllib2
import simplejson
import time
import tweepy
import collections
import networkx as nx
import math
from sets import Set
import matplotlib.pyplot as plt

#Does an OAuth login to access Twitter API using application settings
def OAuth():
    consumer_key = 'CS7ao75neMHDh8uTCJ3Nng'
    consumer_pass = '9xGJIWnjk7KRBi8Rw097KYlKd7sf2svwj9L6FpMIsA'

    access_key = '819221646-iaVneMz5ltxcC9osFmJ9v9D4W4PQBIbG4jZwAXXc'
    access_pass = '4h9VvHttlrWUqGcY8iQ7J0ZYDYCfbO0019BMhWNXkME'

    auth1 = tweepy.auth.OAuthHandler(consumer_key,consumer_pass)
    auth1.set_access_token(access_key,access_pass)

    api = tweepy.API(auth1)
    return api


#Gets tweets
def getTweets(api,celebrity):
    holder = []
    for pg in range(25):
        timeline = api.user_timeline(celebrity, page = pg)
        holder.extend(timeline)
        if len(timeline) == 0:
            break
    return holder

#Returns list of users whom the celebrity mentions in a particular tweet
def getMentions(api,celebrity,tweet):
    handles = collections.Counter()
    text = tweet.text
    text = text.split(" ")
    for part in text:
        if part.__contains__("@"):
            handles[part[1:]] += 1
    return handles

#Returns reply chains, if celebrity is talking to someone or group of people
def getResponses(api,celebrity,tweet):
    handles = collections.Counter()
    reply = tweet.in_reply_to_screen_name
    handles[reply] += 1
    del handles[None]
    return handles
     
#Collects mutual friends of a celebrity
def makeFriends(celebrity, responses, mentions):
    g = nx.Graph()
    mentionskeys = mentions.keys()
    responseskeys = responses.keys()
    for mentioned in mentionskeys:
        g.add_edge(celebrity,mentioned, weight = 1.0/mentions[mentioned], color = 'blue')

    for responded in responseskeys:
        g.add_edge(celebrity,responded, weight = 1.0/responses[responded], color = 'red')
    
    nx.draw(g)
    plt.show()
    return g

def drawInnerCircle(celebrity, responses, mentions):
    totals = collections.Counter()
    totals.update(responses)
    totals.update(mentions)
    size = len(totals.keys())
    topQuarter = size/4
    topQuarter = totals.most_common(topQuarter)
    topQuarter = topQuarter[-1][1]

    nodelistA = []
    nodelistB = []
    
    keys = totals.keys()
    for i in range(size):
        key = keys[i]
        weight = totals[key]
        if weight >= topQuarter:
            nodelistA.append(i)
        else:
            nodelistB.append(i)
        
    
    
    

def main():
    api = OAuth()

    handles = [
    "https://twitter.com/TheRealStanLee",
    "https://twitter.com/megatokyo",
    "https://twitter.com/NEBU_KURO",
    "https://twitter.com/masijacoke85",
    "https://twitter.com/travelchannel",
    "https://twitter.com/Bourdain",
    "https://twitter.com/ciaela",
    "https://twitter.com/petersgreenberg",
    "https://twitter.com/OJessicaNigri",
    "https://twitter.com/AlodiaAlmira",
    "https://twitter.com/ladygaga",
    "https://twitter.com/Oprah",
    "https://twitter.com/kevjumba",
    "https://twitter.com/Machinima_com",
    "https://twitter.com/coollike",
    "https://twitter.com/jfa_nadeshiko",
    "https://twitter.com/usainbolt",
    "https://twitter.com/GordonRamsay01",
    "https://twitter.com/EpicMealTime",
    "https://twitter.com/utadahikaru",
    "https://twitter.com/JayZ",
    "https://twitter.com/masason",
    "https://twitter.com/jack",
    "https://twitter.com/VictorQuest",
    "https://twitter.com/CarnegieMellon",
    "https://twitter.com/LuisvonAhn",
    "https://twitter.com/yun0808",
    "https://twitter.com/touya_skulldy",
    "https://twitter.com/siu3334"
    ]
    handles = [ handle[20:] for handle in handles]

    for celebrity in handles[23:24]:
        user = api.get_user(celebrity)
        timeline = getTweets(api,celebrity)
        print celebrity
        mentions = collections.Counter()
        responses = collections.Counter()
        for tweet in timeline:
            mentions.update(getMentions(api,celebrity,tweet))
            responses.update(getResponses(api,celebrity,tweet))
        print "Mentions", mentions
        print "Responses", responses

        #makeFriends(celebrity,responses,mentions)
        drawInnerCircle(celebrity,responses,mentions)
        '''
        intersection = {}
        conv = mentions.keys()
        for con in conv:
            value = mentions[con]*responses[con]
            value = math.sqrt(value)
            if value > 0:
                intersection[con] = value
        print "Intersection", intersection
        '''
            
            
main()

#'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'text', 'truncated', 'user'
# in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str'
import scraperwiki
import urllib2
import simplejson
import time
import tweepy
import collections
import networkx as nx
import math
from sets import Set
import matplotlib.pyplot as plt

#Does an OAuth login to access Twitter API using application settings
def OAuth():
    consumer_key = 'CS7ao75neMHDh8uTCJ3Nng'
    consumer_pass = '9xGJIWnjk7KRBi8Rw097KYlKd7sf2svwj9L6FpMIsA'

    access_key = '819221646-iaVneMz5ltxcC9osFmJ9v9D4W4PQBIbG4jZwAXXc'
    access_pass = '4h9VvHttlrWUqGcY8iQ7J0ZYDYCfbO0019BMhWNXkME'

    auth1 = tweepy.auth.OAuthHandler(consumer_key,consumer_pass)
    auth1.set_access_token(access_key,access_pass)

    api = tweepy.API(auth1)
    return api


#Gets tweets
def getTweets(api,celebrity):
    holder = []
    for pg in range(25):
        timeline = api.user_timeline(celebrity, page = pg)
        holder.extend(timeline)
        if len(timeline) == 0:
            break
    return holder

#Returns list of users whom the celebrity mentions in a particular tweet
def getMentions(api,celebrity,tweet):
    handles = collections.Counter()
    text = tweet.text
    text = text.split(" ")
    for part in text:
        if part.__contains__("@"):
            handles[part[1:]] += 1
    return handles

#Returns reply chains, if celebrity is talking to someone or group of people
def getResponses(api,celebrity,tweet):
    handles = collections.Counter()
    reply = tweet.in_reply_to_screen_name
    handles[reply] += 1
    del handles[None]
    return handles
     
#Collects mutual friends of a celebrity
def makeFriends(celebrity, responses, mentions):
    g = nx.Graph()
    mentionskeys = mentions.keys()
    responseskeys = responses.keys()
    for mentioned in mentionskeys:
        g.add_edge(celebrity,mentioned, weight = 1.0/mentions[mentioned], color = 'blue')

    for responded in responseskeys:
        g.add_edge(celebrity,responded, weight = 1.0/responses[responded], color = 'red')
    
    nx.draw(g)
    plt.show()
    return g

def drawInnerCircle(celebrity, responses, mentions):
    totals = collections.Counter()
    totals.update(responses)
    totals.update(mentions)
    size = len(totals.keys())
    topQuarter = size/4
    topQuarter = totals.most_common(topQuarter)
    topQuarter = topQuarter[-1][1]

    nodelistA = []
    nodelistB = []
    
    keys = totals.keys()
    for i in range(size):
        key = keys[i]
        weight = totals[key]
        if weight >= topQuarter:
            nodelistA.append(i)
        else:
            nodelistB.append(i)
        
    
    
    

def main():
    api = OAuth()

    handles = [
    "https://twitter.com/TheRealStanLee",
    "https://twitter.com/megatokyo",
    "https://twitter.com/NEBU_KURO",
    "https://twitter.com/masijacoke85",
    "https://twitter.com/travelchannel",
    "https://twitter.com/Bourdain",
    "https://twitter.com/ciaela",
    "https://twitter.com/petersgreenberg",
    "https://twitter.com/OJessicaNigri",
    "https://twitter.com/AlodiaAlmira",
    "https://twitter.com/ladygaga",
    "https://twitter.com/Oprah",
    "https://twitter.com/kevjumba",
    "https://twitter.com/Machinima_com",
    "https://twitter.com/coollike",
    "https://twitter.com/jfa_nadeshiko",
    "https://twitter.com/usainbolt",
    "https://twitter.com/GordonRamsay01",
    "https://twitter.com/EpicMealTime",
    "https://twitter.com/utadahikaru",
    "https://twitter.com/JayZ",
    "https://twitter.com/masason",
    "https://twitter.com/jack",
    "https://twitter.com/VictorQuest",
    "https://twitter.com/CarnegieMellon",
    "https://twitter.com/LuisvonAhn",
    "https://twitter.com/yun0808",
    "https://twitter.com/touya_skulldy",
    "https://twitter.com/siu3334"
    ]
    handles = [ handle[20:] for handle in handles]

    for celebrity in handles[23:24]:
        user = api.get_user(celebrity)
        timeline = getTweets(api,celebrity)
        print celebrity
        mentions = collections.Counter()
        responses = collections.Counter()
        for tweet in timeline:
            mentions.update(getMentions(api,celebrity,tweet))
            responses.update(getResponses(api,celebrity,tweet))
        print "Mentions", mentions
        print "Responses", responses

        #makeFriends(celebrity,responses,mentions)
        drawInnerCircle(celebrity,responses,mentions)
        '''
        intersection = {}
        conv = mentions.keys()
        for con in conv:
            value = mentions[con]*responses[con]
            value = math.sqrt(value)
            if value > 0:
                intersection[con] = value
        print "Intersection", intersection
        '''
            
            
main()

#'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'text', 'truncated', 'user'
# in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str'
import scraperwiki
import urllib2
import simplejson
import time
import tweepy
import collections
import networkx as nx
import math
from sets import Set
import matplotlib.pyplot as plt

#Does an OAuth login to access Twitter API using application settings
def OAuth():
    consumer_key = 'CS7ao75neMHDh8uTCJ3Nng'
    consumer_pass = '9xGJIWnjk7KRBi8Rw097KYlKd7sf2svwj9L6FpMIsA'

    access_key = '819221646-iaVneMz5ltxcC9osFmJ9v9D4W4PQBIbG4jZwAXXc'
    access_pass = '4h9VvHttlrWUqGcY8iQ7J0ZYDYCfbO0019BMhWNXkME'

    auth1 = tweepy.auth.OAuthHandler(consumer_key,consumer_pass)
    auth1.set_access_token(access_key,access_pass)

    api = tweepy.API(auth1)
    return api


#Gets tweets
def getTweets(api,celebrity):
    holder = []
    for pg in range(25):
        timeline = api.user_timeline(celebrity, page = pg)
        holder.extend(timeline)
        if len(timeline) == 0:
            break
    return holder

#Returns list of users whom the celebrity mentions in a particular tweet
def getMentions(api,celebrity,tweet):
    handles = collections.Counter()
    text = tweet.text
    text = text.split(" ")
    for part in text:
        if part.__contains__("@"):
            handles[part[1:]] += 1
    return handles

#Returns reply chains, if celebrity is talking to someone or group of people
def getResponses(api,celebrity,tweet):
    handles = collections.Counter()
    reply = tweet.in_reply_to_screen_name
    handles[reply] += 1
    del handles[None]
    return handles
     
#Collects mutual friends of a celebrity
def makeFriends(celebrity, responses, mentions):
    g = nx.Graph()
    mentionskeys = mentions.keys()
    responseskeys = responses.keys()
    for mentioned in mentionskeys:
        g.add_edge(celebrity,mentioned, weight = 1.0/mentions[mentioned], color = 'blue')

    for responded in responseskeys:
        g.add_edge(celebrity,responded, weight = 1.0/responses[responded], color = 'red')
    
    nx.draw(g)
    plt.show()
    return g

def drawInnerCircle(celebrity, responses, mentions):
    totals = collections.Counter()
    totals.update(responses)
    totals.update(mentions)
    size = len(totals.keys())
    topQuarter = size/4
    topQuarter = totals.most_common(topQuarter)
    topQuarter = topQuarter[-1][1]

    nodelistA = []
    nodelistB = []
    
    keys = totals.keys()
    for i in range(size):
        key = keys[i]
        weight = totals[key]
        if weight >= topQuarter:
            nodelistA.append(i)
        else:
            nodelistB.append(i)
        
    
    
    

def main():
    api = OAuth()

    handles = [
    "https://twitter.com/TheRealStanLee",
    "https://twitter.com/megatokyo",
    "https://twitter.com/NEBU_KURO",
    "https://twitter.com/masijacoke85",
    "https://twitter.com/travelchannel",
    "https://twitter.com/Bourdain",
    "https://twitter.com/ciaela",
    "https://twitter.com/petersgreenberg",
    "https://twitter.com/OJessicaNigri",
    "https://twitter.com/AlodiaAlmira",
    "https://twitter.com/ladygaga",
    "https://twitter.com/Oprah",
    "https://twitter.com/kevjumba",
    "https://twitter.com/Machinima_com",
    "https://twitter.com/coollike",
    "https://twitter.com/jfa_nadeshiko",
    "https://twitter.com/usainbolt",
    "https://twitter.com/GordonRamsay01",
    "https://twitter.com/EpicMealTime",
    "https://twitter.com/utadahikaru",
    "https://twitter.com/JayZ",
    "https://twitter.com/masason",
    "https://twitter.com/jack",
    "https://twitter.com/VictorQuest",
    "https://twitter.com/CarnegieMellon",
    "https://twitter.com/LuisvonAhn",
    "https://twitter.com/yun0808",
    "https://twitter.com/touya_skulldy",
    "https://twitter.com/siu3334"
    ]
    handles = [ handle[20:] for handle in handles]

    for celebrity in handles[23:24]:
        user = api.get_user(celebrity)
        timeline = getTweets(api,celebrity)
        print celebrity
        mentions = collections.Counter()
        responses = collections.Counter()
        for tweet in timeline:
            mentions.update(getMentions(api,celebrity,tweet))
            responses.update(getResponses(api,celebrity,tweet))
        print "Mentions", mentions
        print "Responses", responses

        #makeFriends(celebrity,responses,mentions)
        drawInnerCircle(celebrity,responses,mentions)
        '''
        intersection = {}
        conv = mentions.keys()
        for con in conv:
            value = mentions[con]*responses[con]
            value = math.sqrt(value)
            if value > 0:
                intersection[con] = value
        print "Intersection", intersection
        '''
            
            
main()

#'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'text', 'truncated', 'user'
# in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str'
