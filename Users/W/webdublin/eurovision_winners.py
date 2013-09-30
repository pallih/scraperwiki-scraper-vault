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


html = geocode["parse"]["text"]["*"]

urls = []

root = lxml.html.fromstring(html)
bScrape = 1
for tr in root.cssselect("table tr"):
    #print tr.text
    ths = tr.cssselect("th")
    if len(ths) == 1:
        year = ths[0].cssselect("a")
        if len(year) > 0:
            sYear = year[0].text

    #print year
    tds = tr.cssselect("td")
    if len(tds) == 9:
        if sYear != "2013":
            country = tds[0].cssselect("a")
            song = tds[1].cssselect("a")
            singer = tds[2].cssselect("a")  
            venue =  tds[8].cssselect("a")    
            sSong = song[0].text            
            youtube_url = ''           
                   
            f = {'q' : sSong.encode('utf-8')}
            try:
                year_url = utube + urllib.urlencode(f) + key + utube_end  
            except ValueError as e:
                print e                
                                
            urls.append ([year_url, sYear, country[0].text, song[0].text, singer[0].text,youtube_url, venue[0].get('title'), venue[1].text])
            
count = 0
error = 0

for urlo in urls:
    time.sleep(1)
    json = ""
    try:
        print urlo[1] + "- " + urlo[0]
        json = simplejson.loads(scraperwiki.scrape(urlo[0]))     
        print json
        
        youtube_url = json["feed"]["entry"][0]["media$group"]["media$player"][0]["url"]
        count = count + 1
        
               
        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":youtube_url, "venue_country":urlo[6], "venue_city":urlo[7]})
        
    except ValueError as e:
        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":urlo[0]})
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


html = geocode["parse"]["text"]["*"]

urls = []

root = lxml.html.fromstring(html)
bScrape = 1
for tr in root.cssselect("table tr"):
    #print tr.text
    ths = tr.cssselect("th")
    if len(ths) == 1:
        year = ths[0].cssselect("a")
        if len(year) > 0:
            sYear = year[0].text

    #print year
    tds = tr.cssselect("td")
    if len(tds) == 9:
        if sYear != "2013":
            country = tds[0].cssselect("a")
            song = tds[1].cssselect("a")
            singer = tds[2].cssselect("a")  
            venue =  tds[8].cssselect("a")    
            sSong = song[0].text            
            youtube_url = ''           
                   
            f = {'q' : sSong.encode('utf-8')}
            try:
                year_url = utube + urllib.urlencode(f) + key + utube_end  
            except ValueError as e:
                print e                
                                
            urls.append ([year_url, sYear, country[0].text, song[0].text, singer[0].text,youtube_url, venue[0].get('title'), venue[1].text])
            
count = 0
error = 0

for urlo in urls:
    time.sleep(1)
    json = ""
    try:
        print urlo[1] + "- " + urlo[0]
        json = simplejson.loads(scraperwiki.scrape(urlo[0]))     
        print json
        
        youtube_url = json["feed"]["entry"][0]["media$group"]["media$player"][0]["url"]
        count = count + 1
        
               
        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":youtube_url, "venue_country":urlo[6], "venue_city":urlo[7]})
        
    except ValueError as e:
        scraperwiki.sqlite.save(unique_keys=["year"], data={"year":urlo[1], "country":urlo[2], "song":urlo[3], "singer":urlo[4], "url":urlo[0]})
        print(e)        
        pass