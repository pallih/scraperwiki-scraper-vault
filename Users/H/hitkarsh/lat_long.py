import scraperwiki
import lxml.html
from geopy import geocoders  
import time

def getll(loc):
    g = geocoders.Google(domain='maps.google.co.uk')
    try:
        for place, (lat, lng) in g.geocode(loc,exactly_one=False):
            ltd=lat
            lngt=lng
    except:
        ltd=0
        lngt=0
    return ltd,lngt
l1=['NOIDA']
print len(l1)
sl_no=0
#for i in l1:
 #   #row=[]
  #  #row=i.split(',')
   # lat,lng=getll(i+",India")
    #scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"city":i,"latitude":lat,"longitude":lng})
    #sl_no+=1
    #time.sleep(1)
for i in range(len(l1)):
    #if i<284:
     #   continue
    lat,lng=getll(l1[i]+",India")
    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state":l1[i],"latitude":lat,"longitude":lng})
    sl_no+=1
    time.sleep(1)
import scraperwiki
import lxml.html
from geopy import geocoders  
import time

def getll(loc):
    g = geocoders.Google(domain='maps.google.co.uk')
    try:
        for place, (lat, lng) in g.geocode(loc,exactly_one=False):
            ltd=lat
            lngt=lng
    except:
        ltd=0
        lngt=0
    return ltd,lngt
l1=['NOIDA']
print len(l1)
sl_no=0
#for i in l1:
 #   #row=[]
  #  #row=i.split(',')
   # lat,lng=getll(i+",India")
    #scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"city":i,"latitude":lat,"longitude":lng})
    #sl_no+=1
    #time.sleep(1)
for i in range(len(l1)):
    #if i<284:
     #   continue
    lat,lng=getll(l1[i]+",India")
    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state":l1[i],"latitude":lat,"longitude":lng})
    sl_no+=1
    time.sleep(1)
