import scraperwiki
import tweepy
import datetime

def getTweetCount(search):
    lst = tweepy.api.search(q=search, rpp=1000)
    return len(lst)

def getTwitterStatsForDay(name):
    usr = tweepy.api.get_user(name)
    data = {
            "date":datetime.datetime.now().date(),
            "account":name,
            "followers":usr.followers_count,
            "listed":usr.listed_count,
            "friends":usr.friends_count,
            "tweets":usr.statuses_count,
            "favorites":usr.favourites_count,
            "mentions":getTweetCount("@"+name)
            }
    scraperwiki.sqlite.save(unique_keys=['date','account'], data=data)

getTwitterStatsForDay('mcfruttero')
import scraperwiki
import tweepy
import datetime

def getTweetCount(search):
    lst = tweepy.api.search(q=search, rpp=1000)
    return len(lst)

def getTwitterStatsForDay(name):
    usr = tweepy.api.get_user(name)
    data = {
            "date":datetime.datetime.now().date(),
            "account":name,
            "followers":usr.followers_count,
            "listed":usr.listed_count,
            "friends":usr.friends_count,
            "tweets":usr.statuses_count,
            "favorites":usr.favourites_count,
            "mentions":getTweetCount("@"+name)
            }
    scraperwiki.sqlite.save(unique_keys=['date','account'], data=data)

getTwitterStatsForDay('mcfruttero')
