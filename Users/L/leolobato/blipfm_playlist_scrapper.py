import scraperwiki
import lxml.html
url = "http://blip.fm/profile/leolobato/playlist"
html = scraperwiki.scrape(url)
doc = lxml.html.fromstring(html)
i = 0

for el in doc.cssselect("a.blipTypeIcon"):
    song = el.attrib['title'].replace("\\'", "'").replace("search for ","")
    print song
    data = {
        'row': i,
        'song': song
    }
    scraperwiki.sqlite.save(unique_keys=['row'], data=data)
    i+=1
import scraperwiki
import lxml.html
url = "http://blip.fm/profile/leolobato/playlist"
html = scraperwiki.scrape(url)
doc = lxml.html.fromstring(html)
i = 0

for el in doc.cssselect("a.blipTypeIcon"):
    song = el.attrib['title'].replace("\\'", "'").replace("search for ","")
    print song
    data = {
        'row': i,
        'song': song
    }
    scraperwiki.sqlite.save(unique_keys=['row'], data=data)
    i+=1
