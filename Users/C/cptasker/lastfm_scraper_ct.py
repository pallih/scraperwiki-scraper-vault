import scraperwiki
import lxml.html

# Blank Python

html = scraperwiki.scrape("http://www.last.fm/user/frabcus/tracks")

root = lxml.html.fromstring(html)

for x in root.cssselect("table.tracklist tr"):
    links = x.cssselect("a")
    artist = links[1].text
    track = links[2].text
    url = links[2].get('href')
    print url
    
    scraperwiki.sqlite.save(unique_keys=['url'], data={"artist" : artist, "track" : track})