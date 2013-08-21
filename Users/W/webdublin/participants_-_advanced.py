import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2


# Getting Eurovision 2012 Participants
# scraperwiki.sqlite.save(unique_keys=["country"], data={"country":el.text})
# scraperwiki.sqlite.save(unique_keys=["contestant"], data={"country":el.text))

url = "http://www.eurovision.tv/page/baku-2012/about/shows/participants"           
#scraperwiki.sqlite.execute("delete from swdata") 

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
singer = ""
country = ""
song = ""

contestants = []

record_id = 1
colSinger = 0
colSong = 1
semicount = 0
semi = 1

for el in root.cssselect("td.country a"):
    col = 0
    country = el.text   
   
    for j in root.cssselect("tr.nowinner td"):
        if record_id == 1:
            colSinger = 2
            colSong = 3
        else:
            colSinger = (record_id - 1) * 4 + 2
            colSong = colSinger + 1

        if col == colSinger : 
            singer = j.text
            #print singer

        if col == colSong :
            song = j.text
            break
        else:
            col += 1
    
    #print country +  " - " + singer
    record_id += 1
    
    if semicount >= 18:
        semi = 2

    if semicount >= 36:
        semi = 0

    scraperwiki.sqlite.save(unique_keys=["country"], data={"country":country, "singer":singer, "song":song, "semi":semi})
    print country + " - " + singer
    semicount = semicount + 1
