import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime

def getlistdata (url, lang):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    

    ENGTITLE =[]
    IKSVLINK =[]    
    
    for i, el in enumerate(root.cssselect("#movielist div")):           
        for el1 in el.cssselect("a span"):
            text = el1.text
            anode = el1.getparent()
            link = anode.attrib['href']
            print text, link
            scraperwiki.sqlite.save(unique_keys=["IKSVLINK"], data={lang+"TITLE":text, "IKSVLINK":link})


    return

def getenlistdata (url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    

    ENGTITLE =[]
    IKSVLINK =[]    
    
    for i, el in enumerate(root.cssselect("#movielist div")):           
        for el1 in el.cssselect("a span"):
            text = el1.text
            anode = el1.getparent()
            link = anode.attrib['href']
            print text, link
            scraperwiki.sqlite.save(unique_keys=["ENGTITLE"], data={"ENGTITLE":text, "IKSVLINK":link})


    return


#
#scraperwiki.sqlite.execute("DELETE FROM swdata")
#scraperwiki.sqlite.commit()

baseeng = "http://film.iksv.org/en/filmlistesi"
basetur = "http://film.iksv.org/tr/filmlistesi"


getlistdata(baseeng, "ENG")
getlistdata(basetur, "TUR")




