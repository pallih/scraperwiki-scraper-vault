import scraperwiki

import scraperwiki           
import lxml.html
import time
import datetime

from datetime import datetime, timedelta
from pytz import timezone
import pytz

#def compare (h0, m0, h1,m1)
    #if()

#def findend (h, m, LH, LM)
#    minh = 100
#    minm = 60
#    found= 0

#    for i, el in enumerate(LH):
        #
#        if (LH[i] == h && LM[i] > m):
            
    

def getdata (url, date):
    
    datestr = date.strftime("%d.%m.%Y") 

    url+=datestr

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)


    
    channelname=root.cssselect("tr:nth-child(2) .wd100 .a333333x12")[0].text
    channelname.replace("\r\n                                                        ", "")
    print channelname    


    LT =[]
    LC =[]    
    
    for i, el in enumerate(root.cssselect(".wd274 a")):           
        print i
        print el.text
        LT.append(el.text.strip())
        LC.append(channelname.strip())
    
    LH =[]
    LM =[]
    
    for i, el in enumerate(root.cssselect(".wd70")):           
        if i == 0:
            continue
        LH.append(int(el.text.split('.',2)[0]))
        LM.append(int(el.text.split('.',2)[1]))

    LH.append(30)
    LM.append(0)
    
    #for i, el in enumerate(LH):
        #findend(LH[i],LM[i],LH,LM)  
    
        
    for i, el in enumerate(LT):
        data = {
                'key': str(date.year)+"M"+str(date.month)+"d"+str(date.day)+str(LC[i].replace(" ", ""))+"h"+str(LH[i])+"m"+str(LM[i]),
                'Date': date,
                'Title' : LT[i],
                'StartH' : LH[i],
                'StartM' : LM[i],
                'EndH' : LH[i+1],
                'EndM' : LM[i+1],
                'Channel': LC[i],
            }
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
    
    return



# NATIONAL geographic

def getngdata (url, date):

    dateng = date.strftime("%d%m%y") 
    url+=dateng

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    channelname = "NATGEO"

    tag = "national geographic"

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
        hh = int(el.text.split(':',2)[0])
        if (hh < 8):
            hh +=24
        LH.append(hh)
        LM.append(int(el.text.split(':',2)[1]))

    LH.append(30)
    LM.append(0)

        
    for i, el in enumerate(LT):
        print i
        print el
        data = {

                'key': str(date.year)+"M"+str(date.month)+"d"+str(date.day)+str(LC[i].replace(" ", ""))+"h"+str(LH[i])+"m"+str(LM[i]),
                'Date': date,
                'Title' : LT[i],
                'StartH' : LH[i],
                'StartM' : LM[i],
                'EndH' : LH[i+1],
                'EndM' : LM[i+1],
                'Channel': LC[i]
            }
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
    return

###########################################################################################################################################


#
scraperwiki.sqlite.execute("DELETE FROM swdata")
scraperwiki.sqlite.commit()

base = "http://tv.ekolay.net/programliste.aspx?ptid=0&pzid=0"



# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
print now_utc

# Convert to US/Pacific time zone
now_turkey = now_utc.astimezone(timezone('Europe/Istanbul'))
print now_turkey

date = now_turkey.date()
print date

cids= [3,1,8,7,10,21,4]

baseng = "http://natgeotv.com/tr/yayin-akisi/ngc/"



for i in range(8): 
    if(i>0):
        date += timedelta(days=1)
    print(date) 

    for cid in cids:
        getdata(base+"&knlid="+str(cid)+"&tarih", date)
    
    getngdata(str(baseng), date)