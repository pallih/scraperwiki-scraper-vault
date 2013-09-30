#Script to grab a list of recent hashtag users from Twitter and graph their friendship connections

#NOTE this goes against the spirit of Scraperwiki somewhat, because I am using a view on its own to grab and display the data
#As to why I'm not grabbing the Twitter data into a Scraperwiki db using a Scraperwiki scraper... I'm not sure Twitter T&Cs allow that...

#There is a good chance you can run this on your own machine if you install the necessary libraries (see below).
#To do that, copy all this code and save it in a file on you own computer as test.py
#On a linux or mac, using the terminal on your computer, cd to the directory containing test.py and then enter:
#    python test.py > test.gexf
#The programme should run and the output should be sent to the file test.gexf, which you can then load into Gephi, for example.

#If you want to watch progress, set debug=True
#This will break the XML output of the graph file though..
#...so if you want well formed XML output in the actual view, set debug=False
debug=False

#If you run this script on your own machine, you need to install a couple of libraries first if you haven't already done so

#from the command line: easy_install tweepy
import tweepy
#from the command line: easy_install networkx
import networkx as nx

#We're going to build up a list of folk who've recently used the hashtag
sender_ids=[]

#Some config stuff...
rpp=100 #results per page; 100 is the max
limit=100 #the most tweets we want to return, max 1500
searchterm='#sunflowerjam'

#only grab up to the limit...
if limit>rpp: rpp=limit

#I'm going to use networkx to build up a graph of friend connections between recent searchterm users
DG=nx.DiGraph()
#The advantage of networkx is that we can then easily print out the network in a variety of graph viz tool friendly formats


#run a Twitter search using the tweepy library
for result in tweepy.Cursor(tweepy.api.search,q=searchterm,rpp=rpp).items(limit):
    user_name=result.from_user
    user_id=result.from_user_id
    if user_id not in sender_ids:
        if debug: print 'New user',user_name,user_id
        sender_ids.append(user_id)
        DG.add_node(user_id,label=user_name,name=user_name)


#The next step is to grab the friends of each user (likely to be fewer than their friends, and construct a graph

#Note that we really should keep tabs on how many API calls we have made in case we hit the limit...
#(I think calls to the search API don't count...)
#Each grab of the friends list grabs up to 5k users (I think) but if a user has 20k users, that may use 4 calls etc
# most folk have < 5000 friends, so assume 1 call per friend
# Unauthenticated calls are limited at 150 calls per hour
# Authenticated calls give you 350 per hour
# So as a rule of thumb, if no-one else is running unauthenticated calls from Scraperwiki, run this at most once an hour to pull back
## hashtag networks containing no more than 100 people...

for user in sender_ids:
    #that is, for each unique recent user of the search term...
    if debug: print 'getting friends of',user
    #grab the friends of the current user
    friends=tweepy.Cursor(tweepy.api.friends_ids,id=user).items()
    #we're now going to look through the friends list to see if any friends are recent searchterm users themselves
    for friend in friends:
        if friend in sender_ids:
            #if they are, add them to the graph with an edge from user to friend
            DG.add_edge(user,friend)


#networkx has a variety of file export filters available, such as GEXF
#gexf files can be imported directly into a tool such as Gephi (gephi.org)
import networkx.readwrite.gexf as gf

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

try:
    import scraperwiki
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
except:
    pass

try:
    from xml.etree.cElementTree import tostring
    print tostring(writer.xml)
except:
    print 'You need to find a way of printing out the XML object...'

#If you run/preview this view in scraperwiki, assuming you haven't maxed out on the Twitter API,
##or spent so long runningthe script/waiting that scraperwiki has timed out the script on you,
##you should see an XML based GEXF file. Save it with a .gexf suffix, then open it in something like Gephi... :-)
#Script to grab a list of recent hashtag users from Twitter and graph their friendship connections

#NOTE this goes against the spirit of Scraperwiki somewhat, because I am using a view on its own to grab and display the data
#As to why I'm not grabbing the Twitter data into a Scraperwiki db using a Scraperwiki scraper... I'm not sure Twitter T&Cs allow that...

#There is a good chance you can run this on your own machine if you install the necessary libraries (see below).
#To do that, copy all this code and save it in a file on you own computer as test.py
#On a linux or mac, using the terminal on your computer, cd to the directory containing test.py and then enter:
#    python test.py > test.gexf
#The programme should run and the output should be sent to the file test.gexf, which you can then load into Gephi, for example.

#If you want to watch progress, set debug=True
#This will break the XML output of the graph file though..
#...so if you want well formed XML output in the actual view, set debug=False
debug=False

#If you run this script on your own machine, you need to install a couple of libraries first if you haven't already done so

#from the command line: easy_install tweepy
import tweepy
#from the command line: easy_install networkx
import networkx as nx

#We're going to build up a list of folk who've recently used the hashtag
sender_ids=[]

#Some config stuff...
rpp=100 #results per page; 100 is the max
limit=100 #the most tweets we want to return, max 1500
searchterm='#sunflowerjam'

#only grab up to the limit...
if limit>rpp: rpp=limit

#I'm going to use networkx to build up a graph of friend connections between recent searchterm users
DG=nx.DiGraph()
#The advantage of networkx is that we can then easily print out the network in a variety of graph viz tool friendly formats


#run a Twitter search using the tweepy library
for result in tweepy.Cursor(tweepy.api.search,q=searchterm,rpp=rpp).items(limit):
    user_name=result.from_user
    user_id=result.from_user_id
    if user_id not in sender_ids:
        if debug: print 'New user',user_name,user_id
        sender_ids.append(user_id)
        DG.add_node(user_id,label=user_name,name=user_name)


#The next step is to grab the friends of each user (likely to be fewer than their friends, and construct a graph

#Note that we really should keep tabs on how many API calls we have made in case we hit the limit...
#(I think calls to the search API don't count...)
#Each grab of the friends list grabs up to 5k users (I think) but if a user has 20k users, that may use 4 calls etc
# most folk have < 5000 friends, so assume 1 call per friend
# Unauthenticated calls are limited at 150 calls per hour
# Authenticated calls give you 350 per hour
# So as a rule of thumb, if no-one else is running unauthenticated calls from Scraperwiki, run this at most once an hour to pull back
## hashtag networks containing no more than 100 people...

for user in sender_ids:
    #that is, for each unique recent user of the search term...
    if debug: print 'getting friends of',user
    #grab the friends of the current user
    friends=tweepy.Cursor(tweepy.api.friends_ids,id=user).items()
    #we're now going to look through the friends list to see if any friends are recent searchterm users themselves
    for friend in friends:
        if friend in sender_ids:
            #if they are, add them to the graph with an edge from user to friend
            DG.add_edge(user,friend)


#networkx has a variety of file export filters available, such as GEXF
#gexf files can be imported directly into a tool such as Gephi (gephi.org)
import networkx.readwrite.gexf as gf

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

try:
    import scraperwiki
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
except:
    pass

try:
    from xml.etree.cElementTree import tostring
    print tostring(writer.xml)
except:
    print 'You need to find a way of printing out the XML object...'

#If you run/preview this view in scraperwiki, assuming you haven't maxed out on the Twitter API,
##or spent so long runningthe script/waiting that scraperwiki has timed out the script on you,
##you should see an XML based GEXF file. Save it with a .gexf suffix, then open it in something like Gephi... :-)
