import scraperwiki
import lxml.html
 
url = 'http://www.ryansoccer.com/Ryan_Soccer/Photos/Photos_files/rss.xml'
 
# iPhoto album.
# Scrape albums.
rss = scraperwiki.scrape(url)
root = lxml.html.fromstring(rss)
 
 
record = {}
for album in root.cssselect("item"):
    albumTitle = album.find("title").text
    albumLink = album.find("link").tail 
    if albumLink:
        # Visit the album page RSS feed and scrape the images. 
        albumLink = albumLink.replace(".html", "_files/rss")
        print "Fetching images for " + albumTitle 
        rss = scraperwiki.scrape(albumLink)
        root = lxml.html.fromstring(rss)
        for image in root.cssselect("item enclosure"):
            record["url"] = image.attrib['url']
            #record["thumbnail_url"] = image.find("thumbnail").text
            #record["title"] = image.find("title").text
            #record["album_title"] = albumTitle
            scraperwiki.sqlite.save(["url"], record)
 
exit()