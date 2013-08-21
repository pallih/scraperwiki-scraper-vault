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
    
    for i, el in enumerate(root.cssselect(".ScheduleDayTitle")):           
        txt = ""
        for sel in el.cssselect("span"):
            txt+=" "+sel.text
        print txt      
        LT.append(txt)
        LC.append(channelname)
    
    LH =[]
    LM =[]
    
    for i, el in enumerate(root.cssselect(".ScheduleDayHour")):           
        print el.text
        LH.append(int(el.text.split(':',2)[0]))
        LM.append(int(el.text.split(':',2)[1]))

        
    for i, el in enumerate(LT):
        print i
        print el
        data = {
                'key': str(LC[i])+str(i),
                'Title' : LT[i],
                'StartH' : LH[i],
                'StartM' : LM[i],
                'Channel': LC[i]
            }
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
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




