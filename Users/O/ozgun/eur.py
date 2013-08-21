import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime


def geteurdata (url, datestr):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    dateid = "#proglist_0_" + datestr

    channelname = "Eurosport"

    LT =[]
    LC =[]    
    
    
    for i, el in enumerate(root.cssselect(dateid + " .emissionFull")):           
        print el.text      
        LT.append(el.text)
        LC.append(channelname)
    
    LH =[]
    LM =[]
    
    for i, el in enumerate(root.cssselect(dateid +" .heureFull")):           
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

base = "http://tr.eurosport.com/tvschedule.shtml"

today = datetime.date.today()
dateeur = today.strftime("%d%m%Y") 

geteurdata(base, dateeur)




