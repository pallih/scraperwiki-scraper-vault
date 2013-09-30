import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime


def getngdata (url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    channelname = "NATGEO"

    LT =[]
    LC =[]    
    
    for i, el in enumerate(root.cssselect("font font:nth-child(1)")):           
        print el
    return


#
#scraperwiki.sqlite.execute("DELETE FROM swdata")
#scraperwiki.sqlite.commit()

baseng = "http://natgeotv.com/tr/yayin-akisi/ngc/"

today = datetime.date.today(tzinfo=utc)
today = today.astimezone("+2:00")
print today

dateng = today.strftime("%d%m%y") 

# "08.08.2012"

getngdata(str(baseng)+str(dateng))




import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime


def getngdata (url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    channelname = "NATGEO"

    LT =[]
    LC =[]    
    
    for i, el in enumerate(root.cssselect("font font:nth-child(1)")):           
        print el
    return


#
#scraperwiki.sqlite.execute("DELETE FROM swdata")
#scraperwiki.sqlite.commit()

baseng = "http://natgeotv.com/tr/yayin-akisi/ngc/"

today = datetime.date.today(tzinfo=utc)
today = today.astimezone("+2:00")
print today

dateng = today.strftime("%d%m%y") 

# "08.08.2012"

getngdata(str(baseng)+str(dateng))




