import scraperwiki
import urllib
import feedparser
import datetime
from calendar import weekday
import lxml.html
import tweepy

weekdays =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def getTweetCount(search):
    if search !='':
        this = '"{srch}"'.format(srch=search)
        lst = tweepy.api.search(q=this, rpp=100)
        return len(lst)
    else: return 0

def getWordCount(string):
    count = 0
    root = lxml.html.fromstring(string)
    content = root.xpath('//text()')
    for text in content:count += text.count(' ')
    return count

def getData(e):
    if ',' in e.author: auths = e.author.split(',')
    else: auths=[e.author]
    t = e.date_parsed
    d = datetime.date(t.tm_year,t.tm_mon,t.tm_mday)
    for auth in auths: 
        author = auth.strip()
        data ={
              'author':author,
              'authorTweetCount':getTweetCount(author),
              'weekday':weekdays[d.weekday()],
              'date':d,
              'categoryCount':len(e.categories),
              'wordCount':getWordCount(e.description),
              'articleCount':1
              }
    return data

def GuardianMusicBlogScrape():
    d = feedparser.parse("http://linkea.do/feed")
    for e in d.entries:
        data = getData(e)
        scraperwiki.sqlite.save(unique_keys=['date','author'], data=data)
        #print data

GuardianMusicBlogScrape()
import scraperwiki
import urllib
import feedparser
import datetime
from calendar import weekday
import lxml.html
import tweepy

weekdays =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def getTweetCount(search):
    if search !='':
        this = '"{srch}"'.format(srch=search)
        lst = tweepy.api.search(q=this, rpp=100)
        return len(lst)
    else: return 0

def getWordCount(string):
    count = 0
    root = lxml.html.fromstring(string)
    content = root.xpath('//text()')
    for text in content:count += text.count(' ')
    return count

def getData(e):
    if ',' in e.author: auths = e.author.split(',')
    else: auths=[e.author]
    t = e.date_parsed
    d = datetime.date(t.tm_year,t.tm_mon,t.tm_mday)
    for auth in auths: 
        author = auth.strip()
        data ={
              'author':author,
              'authorTweetCount':getTweetCount(author),
              'weekday':weekdays[d.weekday()],
              'date':d,
              'categoryCount':len(e.categories),
              'wordCount':getWordCount(e.description),
              'articleCount':1
              }
    return data

def GuardianMusicBlogScrape():
    d = feedparser.parse("http://linkea.do/feed")
    for e in d.entries:
        data = getData(e)
        scraperwiki.sqlite.save(unique_keys=['date','author'], data=data)
        #print data

GuardianMusicBlogScrape()
