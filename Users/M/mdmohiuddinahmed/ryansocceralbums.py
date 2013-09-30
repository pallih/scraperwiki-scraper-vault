import scraperwiki
import lxml.html
 
url = 'http://www.ryansoccer.com/Ryan_Soccer/Home.html'
 
# iPhoto album.
# Scrape albums.
rss = scraperwiki.scrape(url)
root = lxml.html.fromstring(rss)
 
 
record = {}
        for image in root.iterfind(".//item"):
            record["url"] = image.find("enclosure").get("url")
            record["thumbnail_url"] = image.find("thumbnail").text
            record["title"] = image.find("title").text
            record["album_title"] = albumTitle
            scraperwiki.sqlite.save(["url"], record)
 
exit()
