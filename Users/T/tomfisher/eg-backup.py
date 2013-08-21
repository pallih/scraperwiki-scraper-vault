import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
import lxml.etree



a = 1 

def getposts( url ): #this function collects all posts from a the forum post passed to it in the URL and stores them in the db
    html = scraperwiki.scrape(url) # bind the relevant url
    root = lxml.html.fromstring(html) # turn it into an lxml object
    posttitle = root.cssselect("h2.title.icon")
    for el in posttitle:
        title = el.text_content()
    print title
    for el in root.cssselect("blockquote.postcontent.restore"):
        print "-----new element-----------------------------------------------------"
        children = el.getchildren()
        print el.text_content()
        print "There are also a total of " + str(len(el.cssselect("div.quote_container"))) + " quotes"
        for everychild in children:
            print "This is a child:"
            print everychild.text_content()
        for text in el.itertext():
            print repr(text)
    return

scraperwiki.sqlite.attach("eg-collectposttitles", "src")

list = scraperwiki.sqlite.select("link from src.swdata limit 2 offset 0")


for link in list:
    stringlink = str(link)
    stringlink = stringlink.replace(' ', '')[:-2]
    stringlink = stringlink[11:]
    getposts(stringlink)
