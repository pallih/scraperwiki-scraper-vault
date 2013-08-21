import scraperwiki
from lxml import etree
import dateutil.parser

username = "bharathos"
api_key = "cefce313aa31d3612f8dbd35184a94fc"
pageNumber = 1

# RUNS THROUGH ALL SCROBBLES! remember to indent code when used
allPages = range(1,10)
for pageNumber in reversed(allPages):

    root_page = scraperwiki.scrape("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key="+ api_key + "&user=" + username + "&extended=1&limit=200&page=" + str(pageNumber))
    root = etree.fromstring(root_page)
    tracks = root.find("recenttracks").findall("track")
    
    for track in reversed(tracks):
        # Only record tracks that have been 'loved'
        isLoved = track.find("loved").text
        if isLoved == "0": 
            continue
    
        artist = track.find("artist").find("name").text
        name = track.find("name").text
        link = track.find("url").text
        cover = track.findall("image")[-1].text
        
        try:
            firstScrobble = dateutil.parser.parse(track.find("date").text)
        except:
            firstScrobble = '0'
    
        try:
            # Only record if the track has never been recorded
            exists = scraperwiki.sqlite.select("* from swdata WHERE link='" + link + "' limit 1")
            if len(exists) == 0:
                scraperwiki.sqlite.save(unique_keys=['link'], data={"artist":artist, "track":name, "link":link, "cover":cover, "firstScrobbledOn":firstScrobble})
                print artist + " - " + name + " scrobbled on " + str(firstScrobble)
        except:
            scraperwiki.sqlite.save(unique_keys=['link'], data={"artist":artist, "track":name, "link":link, "cover":cover, "firstScrobbledOn":firstScrobble})
            print artist + " - " + name + " scrobbled on " + str(firstScrobble)

'''
# Can be used to delete a particular track in this case named Parentheses
scraperwiki.sqlite.execute("DELETE from swdata WHERE track='Thrift Shop (feat. Wanz)'")
scraperwiki.sqlite.commit()
'''
