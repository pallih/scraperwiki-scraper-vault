url = 'http://www.umsonst-und-draussen.de/programm.html'

import scraperwiki
import urllib
import lxml.html 

html= scraperwiki.scrape(url)
root= lxml.html.fromstring(html)

eventlist = root.cssselect("div[id='colRight']")[0]
eventnodes = eventlist.getchildren()

for node in eventnodes:
    if node.find("h4") != None:
        day=node.find("h4").text
    if node.find("h3") != None:
        stage=node.find("h3").text
    lis=node.getiterator("li")
    if lis != None:
        for eventli in lis:
            event = {
                "tag" : day,
                "buehne" : stage.title(),
                "link" : "http://umsonst-und-draussen.de/"+eventli.find("a").get("href"),
                "zeit" : eventli.find("span").text[1:6],
                "event" : eventli.find("a").text.title(),
                "beschreibung" : eventli.find("a").tail,
                "id" : day+eventli.find("span").text
            }
            print event
            scraperwiki.sqlite.save(unique_keys=['id'], data=event)

