import cStringIO
import feedparser
import Image
import lxml.html
import scraperwiki
import urllib

d = feedparser.parse("http://feed.500px.com/500px-best")
print d
print d.feed
print d.entries

for entry in d.entries:
    print entry.feedburner_origlink
    print entry.updated
    print entry.title
    print entry.link
    html = scraperwiki.scrape(entry.link)
    root = lxml.html.fromstring(html)
    photo = root.cssselect("div#photo a")
    if len(photo) > 0:
        image_url = photo[0].attrib['href']
        print image_url
        image_name = entry.link.split('/')[-1] + '.jpg'
        print image_name

        image_handle = urllib.urlopen(image_url)
        image = Image.open(cStringIO.StringIO(image_handle.read()))

        #print image.info
        
        scraperwiki.sqlite.save(unique_keys=["link"], data={"link":entry.link,
                                                            "title":entry.title,
                                                            "image_name":image_name,
                                                            "image":list(image.getdata()),
                                                            "published":entry.updated})
        
        del imageimport cStringIO
import feedparser
import Image
import lxml.html
import scraperwiki
import urllib

d = feedparser.parse("http://feed.500px.com/500px-best")
print d
print d.feed
print d.entries

for entry in d.entries:
    print entry.feedburner_origlink
    print entry.updated
    print entry.title
    print entry.link
    html = scraperwiki.scrape(entry.link)
    root = lxml.html.fromstring(html)
    photo = root.cssselect("div#photo a")
    if len(photo) > 0:
        image_url = photo[0].attrib['href']
        print image_url
        image_name = entry.link.split('/')[-1] + '.jpg'
        print image_name

        image_handle = urllib.urlopen(image_url)
        image = Image.open(cStringIO.StringIO(image_handle.read()))

        #print image.info
        
        scraperwiki.sqlite.save(unique_keys=["link"], data={"link":entry.link,
                                                            "title":entry.title,
                                                            "image_name":image_name,
                                                            "image":list(image.getdata()),
                                                            "published":entry.updated})
        
        del image