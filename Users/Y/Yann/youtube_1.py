#import relevant libraries
import scraperwiki
import gdata.youtube
import gdata.youtube.service
import time
import datetime


yt_service = gdata.youtube.service.YouTubeService()

authorSet=['normanfaitdesvideos','MonsieurDream','HugoToutSeul','mistervofficial','BrefCanalPlusTV']
#authorSet=['normanfaitdesvideos','MonsieurDream','HugoToutSeul']

scraperwiki.sqlite.attach("youtube_1")

def LogEntryDetails(entry):
  title=entry.media.title.text
  pubDate=entry.published.text
  description=entry.media.description.text
  viewcount=int(entry.statistics.view_count)
  fav=int(entry.statistics.favorite_count)
  comm=int(entry.comments.feed_link[0].count_hint)
  rating=float(entry.rating.average)
  numraters=int(entry.rating.num_raters)
  t=time.time()
  da=datetime.date.today()
  url=entry.media.player.url

  data1 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE url=? 
    AND date=date('now','-1 day')
    order by timestamp desc limit 1''',url
  )
#pour initier mettre les cnq lignes ci dessus en commentaire et activer celle qui suit
#  data1=""
  if data1=="":
           data = {
                     'author': aut,
                     'title': title,
                     'pubDate': pubDate,
                     'description' : description,
                     'viewcount' : viewcount,
                     'fav': fav,
                     'comm': comm,
                     'rating': rating,
                     'numraters' : numraters,
                     'timestamp' : t,
                     'date' : da,
                     'url' : url
           }
           scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="djeuns") 
  else:
          for d in data1:
               viewcountDV=round(100*(float(viewcount)-float(d["viewcount"]))/(float(d["viewcount"])),1)
               favDV=round(100*(float(fav)-float(d["fav"]))/(float(d["fav"])),1)
               ratingDV=round(100*(float(rating)-float(d["rating"]))/(float(d["rating"])),1)
               commDV=round(100*(float(comm)-float(d["comm"]))/(float(d["comm"])),1)
               numratersDV=round(100*(float(numraters)-float(d["numraters"]))/(float(d["numraters"])),1)
               data = {
                     'author': aut,
                     'title': title,
                     'pubDate': pubDate,
                     'description' : description,
                     'viewcount' : viewcount,
                     'fav': fav,
                     'comm': comm,
                     'rating': rating,
                     'numraters' : numraters,
                     'timestamp' : t,
                     'date' : da,
                     'url' : url,
                     'viewcountDV' : viewcountDV,
                     'favDV' : favDV,                 
                     'commDV' : commDV,
                     'ratingDV' : ratingDV
               }
               scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="djeuns") 



def GetAndLogVideoFeed(uri):
  yt_service = gdata.youtube.service.YouTubeService()
  feed = yt_service.GetYouTubeVideoFeed(uri)
  for entry in feed.entry:
    LogEntryDetails(entry)

def LogVideoFeed(feed):
  for entry in feed.entry:
    LogEntryDetails(entry)


def GetAndLogUserUploads(username):
  yt_service = gdata.youtube.service.YouTubeService()
  uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
  LogVideoFeed(yt_service.GetYouTubeVideoFeed(uri))


for aut in authorSet:
    GetAndLogUserUploads(aut)
#import relevant libraries
import scraperwiki
import gdata.youtube
import gdata.youtube.service
import time
import datetime


yt_service = gdata.youtube.service.YouTubeService()

authorSet=['normanfaitdesvideos','MonsieurDream','HugoToutSeul','mistervofficial','BrefCanalPlusTV']
#authorSet=['normanfaitdesvideos','MonsieurDream','HugoToutSeul']

scraperwiki.sqlite.attach("youtube_1")

def LogEntryDetails(entry):
  title=entry.media.title.text
  pubDate=entry.published.text
  description=entry.media.description.text
  viewcount=int(entry.statistics.view_count)
  fav=int(entry.statistics.favorite_count)
  comm=int(entry.comments.feed_link[0].count_hint)
  rating=float(entry.rating.average)
  numraters=int(entry.rating.num_raters)
  t=time.time()
  da=datetime.date.today()
  url=entry.media.player.url

  data1 = scraperwiki.sqlite.select(
    '''* from youtube_1.djeuns 
    WHERE url=? 
    AND date=date('now','-1 day')
    order by timestamp desc limit 1''',url
  )
#pour initier mettre les cnq lignes ci dessus en commentaire et activer celle qui suit
#  data1=""
  if data1=="":
           data = {
                     'author': aut,
                     'title': title,
                     'pubDate': pubDate,
                     'description' : description,
                     'viewcount' : viewcount,
                     'fav': fav,
                     'comm': comm,
                     'rating': rating,
                     'numraters' : numraters,
                     'timestamp' : t,
                     'date' : da,
                     'url' : url
           }
           scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="djeuns") 
  else:
          for d in data1:
               viewcountDV=round(100*(float(viewcount)-float(d["viewcount"]))/(float(d["viewcount"])),1)
               favDV=round(100*(float(fav)-float(d["fav"]))/(float(d["fav"])),1)
               ratingDV=round(100*(float(rating)-float(d["rating"]))/(float(d["rating"])),1)
               commDV=round(100*(float(comm)-float(d["comm"]))/(float(d["comm"])),1)
               numratersDV=round(100*(float(numraters)-float(d["numraters"]))/(float(d["numraters"])),1)
               data = {
                     'author': aut,
                     'title': title,
                     'pubDate': pubDate,
                     'description' : description,
                     'viewcount' : viewcount,
                     'fav': fav,
                     'comm': comm,
                     'rating': rating,
                     'numraters' : numraters,
                     'timestamp' : t,
                     'date' : da,
                     'url' : url,
                     'viewcountDV' : viewcountDV,
                     'favDV' : favDV,                 
                     'commDV' : commDV,
                     'ratingDV' : ratingDV
               }
               scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="djeuns") 



def GetAndLogVideoFeed(uri):
  yt_service = gdata.youtube.service.YouTubeService()
  feed = yt_service.GetYouTubeVideoFeed(uri)
  for entry in feed.entry:
    LogEntryDetails(entry)

def LogVideoFeed(feed):
  for entry in feed.entry:
    LogEntryDetails(entry)


def GetAndLogUserUploads(username):
  yt_service = gdata.youtube.service.YouTubeService()
  uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
  LogVideoFeed(yt_service.GetYouTubeVideoFeed(uri))


for aut in authorSet:
    GetAndLogUserUploads(aut)
