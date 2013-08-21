import scraperwiki

'''
# Blank Python
#AIM to write code and justify each line with at least 10 source references - To gauge level of effort rather than just copy and pasting code. James would like to see how you adapted the code from an original source to show creative thinking. 

SETUP PHASE:
To utilise TWITTER MODULE (class.methods(object or variable name that defines context)=twitter_api.trends())
this inititiates a HTTP call to GET http://api.twitter.com/trends/1.json

#Mini Project 2 - Python, Twitter and Data visualisation

The following assignment is based upon the Sandbox guest lectures on python, twitter and Data visualisation. This is a programming and analysis assignment as such you are expected to liberally comment your code to describe what you are doing at each step, how you identify the sender of each tweet, and how you avoided naming each tweet sender more than once.  

You will be required to run a demonstration of your code and explain how it works as part of your assessment.

Issue Date 19th December 2012        Submission Date 22nd January 2012

Resources for this assignment can be found on my webpage 

http://doc.gold.ac.uk/~mas01jo/

1.    Using the Twitter API and a Python script or otherwise, search for up to 1500 recent tweets around a particular event or topic based hashtag. (Try to identify a hashtag that has a "small" number of participants (10s to 100s) who send tweets to each other at least some of the time.

Examples might be hastags on the following subjects:
Politics, Football fans, Online Debates, fan Reviews, events.

20 Marks

2.    Write a Python routine that will loop through each of the search results, identify the distinct users who sent the tweet and a count of the number of tweets send by each of them in the sample you collected. 

15 Marks


3.    Extend your program to print out (or save to a file) a sorted league table showing the top 10 tweeters, along with their rank position by tweet volume and a count of the number of tweets they sent.
  
15 Marks


4.    Visualise this data using datawrapper.de or a spreadsheet programme such as Google Sheets to produce a bar chart showing the top 10 tweeters along with the number of tweets each of them sent.  

10 Marks

5.    Optional extension: Tweets that start with a Twitter ID may be thought of as "conversational", specifically tweets that are referred to one user by another who starts a tweet with that particular user's name. For each "conversational" tweet, extract who sent the tweet and to whom, and produce two more league tables: 

i)    showing an ordered ranking of who sent the most conversational tweets 
ii)     showing an ordered ranking of who received the most conversational tweets. 

20 Marks 

6.    Identify how many unique (sender,receiver) pairings there are in your sample (a weak measure of conversational diversity), and produce an ordered league table that displays how many times each conversational pairing was observed in the sampled dataset. 

20 Mark
'''



from scraperwiki import swimport
from scraperwiki.sqlite import save, select
search = swimport('twitter_search').search

# Broad search
search(['#helicopter'])



# Summary statistics
hombre = select('from_user, count(*) as "tweet count" from `swdata` group by from_user')
save(['from_user'], hombre, 'counts-by-user')