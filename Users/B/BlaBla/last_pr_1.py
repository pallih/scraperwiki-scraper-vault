import scraperwiki
from lxml import etree
import dateutil.parser

username = "AnotherBas"
api_key = "d940d5f697ca553c4b60e00fdcb9b972"
pageNumber = 1

allPages = range(1,2)
for pageNumber in (allPages):

    root_page = scraperwiki.scrape("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key="+ api_key + "&user=" + username + "&extended=1&limit=200&page=" + str(pageNumber))
    root = etree.fromstring(root_page)
    tracks = root.find("recenttracks").findall("track")
    
    for track in (tracks):
    
        artist = track.find("artist").find("name").text
        name = track.find("name").text
        link = track.find("url").text
        cover = track.findall("image")[-1].text
            
        scraperwiki.sqlite.save(unique_keys=['date'], data={"artist":artist, "track":name, "link":link, "cover":cover})




