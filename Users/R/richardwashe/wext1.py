import scraperwiki 
import lxml.html

html = scraperwiki.scrape("http://video-a-la-demande.orange.fr/catalog/vod/subCategory/19/Action.html#vod%2FsubCategory%2F19") 

root = lxml.html.fromstring(html)
for el in root: 
    print el.tag 
    for el2 in el: 
        print "--", el2.tag, el2.attrib
        for el3 in el2:
            print "----", el3.tag, el3.attrib
