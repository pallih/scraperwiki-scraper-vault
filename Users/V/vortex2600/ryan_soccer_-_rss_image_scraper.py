import scraperwiki
import lxml.html

url = 'http://www.ryansoccer.com/Ryan_Soccer/Photos/Photos_files/rss.xml'

# iPhoto album.
# Scrape albums.
rss = scraperwiki.scrape(url)
root = lxml.html.fromstring(rss)
#print lxml.etree.tostring(root, pretty_print = True)

record = {}
for album in root.iterfind(".//item"):
    albumTitle = album.find("title").text
    albumLink = album.find("link").tail # Not sure why this isn't parsing correctly, but the tail will get the value.
    if albumLink:
        # Visit the album page RSS feed and scrape the images. 
        albumLink = albumLink.replace(".html", "_files/rss")
        print "Fetching images for " + albumTitle 
        rss = scraperwiki.scrape(albumLink)
        root = lxml.html.fromstring(rss)
        for image in root.iterfind(".//item"):
            test = image.find("title").text
            record["url"] = image.find("enclosure").get("url")
            record["thumbnail_url"] = image.find("thumbnail").text
            record["title"] = image.find("title").text
            record["album_title"] = albumTitle
            scraperwiki.sqlite.save(["url"], record)

exit()

