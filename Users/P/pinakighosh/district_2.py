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
l1=[['Nagaland','Mon'],['Nagaland','Tuensang'],['Nagaland','Mokokchung'],['Nagaland','Zunheboto'],['Nagaland','Wokha'],['Nagaland','Dimapur'],
['Nagaland','Mon'],['Nagaland','Kohima'],['Nagaland','Phek'],['Daman and Diu','Diu'],['Daman and Diu','Daman'],['Chandigarh','Chandigarh']]
sl_no=1
for i in l1:
    lat,lng=getll(i[1]+",India")
    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"city":i[0],"state":i[1],"latitude":lat,"longitude":lng})
    sl_no+=1
    time.sleep(1)