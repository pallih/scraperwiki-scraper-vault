import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import json
import lxml.html           
import socket
import time
from twisted.web import client
from twisted.internet import reactor, defer

# Getting Eurovision Winners from Wikipedia
#title = "List_of_Eurovision_Song_Contest_winners"
url = "http://www.dublinparacon.com/euro.html"
#url = "http://www.dublin24.com/scraper_files/euro.html"
ujson = "http://www.dublinparacon.com/youtube.html"
utube = "https://gdata.youtube.com/feeds/api/videos?"
ujson = "http://www.dublinparacon.com/youtube.html"
utube = "https://gdata.youtube.com/feeds/api/videos?"
utube_end = "&start-index=1&max-results=1&alt=json&"
key="&key=AI39si4VMH0YTMpZ-1ifdH2_ABKc-FrSdun4TixCFZRKAUxMX0DIXkRT_EPuX17aAxZKA1VA-aNbia2FAJ8a91YcCdk4Jw44Hg"
empty_url = ""

georeq = urllib2.Request(url)
geo_response = urllib2.urlopen(georeq)
geocode = simplejson.loads(geo_response.read())

scraperwiki.sqlite.attach("eurovision_2013_-_participants")
participants = scraperwiki.sqlite.select("country, song, singer, 0 'mentions', semi from [eurovision_2013_-_participants].swdata")

urls = []
youtube_url = '' 
count = 0
for part in participants:
    song = part['song']
    sSong = song.lstrip()
    singer = part['singer']
    country = part['country']
    if count == 36:
        f = {'q' : "L'enfer Et Moi eurovision"}
    elif count != 36:
        f = {'q' : sSong.encode('utf-8')+ " eurovision" }
    try:
        year_url = utube + urllib.urlencode(f) + key + utube_end  
    except ValueError as e:
        print e                
                                
    urls.append ([country, sSong, singer, year_url])

count = 0
error = 0

for urlo in urls:
    time.sleep(1)
    json = ""
    try:
        #print urlo[1] + "- " + urlo[0]
        if count == 36:
            print "bogey url" + urlo[3]
        else:
            json = simplejson.loads(scraperwiki.scrape(urlo[3]))     
        print json
        
        try:
            youtube_url = json["feed"]["entry"][0]["media$group"]["media$player"][0]["url"]
            scraperwiki.sqlite.save(unique_keys=["country"], data={"country":urlo[0], "song":urlo[1], "singer":urlo[2], "url":youtube_url})
        except ValueError as e:
            youtube_url = "None Available"
        
        print count
        #print youtube_url
        
        count = count + 1
        
               
#        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":youtube_url, "venue_country":urlo[6], "venue_city":urlo[7]})
        
    except ValueError as e:
#        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":urlo[0]})
        print(e)        
        passimport scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
import json
import lxml.html           
import socket
import time
from twisted.web import client
from twisted.internet import reactor, defer

# Getting Eurovision Winners from Wikipedia
#title = "List_of_Eurovision_Song_Contest_winners"
url = "http://www.dublinparacon.com/euro.html"
#url = "http://www.dublin24.com/scraper_files/euro.html"
ujson = "http://www.dublinparacon.com/youtube.html"
utube = "https://gdata.youtube.com/feeds/api/videos?"
ujson = "http://www.dublinparacon.com/youtube.html"
utube = "https://gdata.youtube.com/feeds/api/videos?"
utube_end = "&start-index=1&max-results=1&alt=json&"
key="&key=AI39si4VMH0YTMpZ-1ifdH2_ABKc-FrSdun4TixCFZRKAUxMX0DIXkRT_EPuX17aAxZKA1VA-aNbia2FAJ8a91YcCdk4Jw44Hg"
empty_url = ""

georeq = urllib2.Request(url)
geo_response = urllib2.urlopen(georeq)
geocode = simplejson.loads(geo_response.read())

scraperwiki.sqlite.attach("eurovision_2013_-_participants")
participants = scraperwiki.sqlite.select("country, song, singer, 0 'mentions', semi from [eurovision_2013_-_participants].swdata")

urls = []
youtube_url = '' 
count = 0
for part in participants:
    song = part['song']
    sSong = song.lstrip()
    singer = part['singer']
    country = part['country']
    if count == 36:
        f = {'q' : "L'enfer Et Moi eurovision"}
    elif count != 36:
        f = {'q' : sSong.encode('utf-8')+ " eurovision" }
    try:
        year_url = utube + urllib.urlencode(f) + key + utube_end  
    except ValueError as e:
        print e                
                                
    urls.append ([country, sSong, singer, year_url])

count = 0
error = 0

for urlo in urls:
    time.sleep(1)
    json = ""
    try:
        #print urlo[1] + "- " + urlo[0]
        if count == 36:
            print "bogey url" + urlo[3]
        else:
            json = simplejson.loads(scraperwiki.scrape(urlo[3]))     
        print json
        
        try:
            youtube_url = json["feed"]["entry"][0]["media$group"]["media$player"][0]["url"]
            scraperwiki.sqlite.save(unique_keys=["country"], data={"country":urlo[0], "song":urlo[1], "singer":urlo[2], "url":youtube_url})
        except ValueError as e:
            youtube_url = "None Available"
        
        print count
        #print youtube_url
        
        count = count + 1
        
               
#        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":youtube_url, "venue_country":urlo[6], "venue_city":urlo[7]})
        
    except ValueError as e:
#        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":urlo[0]})
        print(e)        
        pass