import scraperwiki
import mechanize
import lxml.html
import re

#Bolierplateremoval

br = mechanize.Browser()

url = "http://derstandard.at/1363708075014/Berichte-ueber-Explosionen-bei-Boston-Marathon"

response = br.open(url)
root = lxml.html.fromstring(response.read())

def checkP(root):
    div = root.cssselect("div")
    for div in div:
        if len(div.cssselect("h1")) or len(div.cssselect("h2")) > 0:
            print "-------------------------------"
            NOTCONTENT = False
            print div.text_content()
            for p in div.cssselect("p"):
                print len(p.text_content().split(" ")) , "num of words"
                if len(p.text_content().split(" ")) == 1:
                    NOTCONTENT = True
                print len(p.text_content().split(".")) , "num of scentences"
                if len(p.text_content().split(".")) == 1:
                    NOTCONTENT = True
            if not NOTCONTENT:
                print "this is it " , div.text_content()
        
checkP(root)        
        