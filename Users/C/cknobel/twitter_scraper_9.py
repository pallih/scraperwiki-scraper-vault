import scraperwiki

import urllib
import json
import re
 
num_tweets = 200
 
resp = urllib.urlopen("https://api.twitter.com/1/statuses/user_timeline.json?screen_name=nytimes&count=" + str(num_tweets))
tweets = json.loads(resp.read())
 
print tweets
 
file1 = open("nyt1.txt", "w")
file2 = open("nyt2.txt", "w")
file3 = open("nyt3.txt", "w")
file4 = open("nyt4.txt", "w")
 
i = 0
for tweet in tweets:
  output_str = tweet['text']
  if '@' in tweet['text']:
    continue
  if 'http' in tweet['text']:
    output_str = re.sub(r'\bhttp\S+\b', '', tweet['text'])
 
  output_str = output_str + "\n"
 
  if i < 50:
    file1.write(output_str.encode('ascii', 'ignore'))
  elif i < 100:
    file2.write(output_str.encode('ascii', 'ignore'))
  elif i < 150:
    file3.write(output_str.encode('ascii', 'ignore'))
  else:
    file4.write(output_str.encode('ascii', 'ignore'))
 
  i += 1
 
resp = urllib.urlopen("https://api.twitter.com/1/statuses/user_timeline.json?screen_name=foxnews&count=" + str(num_tweets))
tweets = json.loads(resp.read())
 
print tweets
 
file1 = open("fox1.txt", "w")
file2 = open("fox2.txt", "w")
file3 = open("fox3.txt", "w")
file4 = open("fox4.txt", "w")
 
i = 0
for tweet in tweets:
  output_str = tweet['text']
  if '@' in tweet['text']:
    continue
  if 'http' in tweet['text']:
    output_str = re.sub(r'\bhttp\S+\b', '', tweet['text'])
 
  output_str = output_str + "\n"
 
  if i < 50:
    file1.write(output_str.encode('ascii', 'ignore'))
  elif i < 100:
    file2.write(output_str.encode('ascii', 'ignore'))
  elif i < 150:
    file3.write(output_str.encode('ascii', 'ignore'))
  else:
    file4.write(output_str.encode('ascii', 'ignore'))
 
  i += 1