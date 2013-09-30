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
state=['Haryana', 'Punjab', 'Goa', 'Kerala', 'Dadra & Nagar Haveli', 'Jammu And Kashmir', 'Maharastra', 'Bihar', 'Assam', 'Chandigarh', 'Jharkhand', 'Meghalaya', 'Orissa', 'Daman & Diu', 'Madhya Pradesh', 'Lakshadweep', 'Manipur', 'Rajasthan', 'NCT of Delhi', 'Tamil Nadu', 'Sikkim', 'West Bengal', 'Andhra Pradesh', 'Himachal Pradesh', 'Nagaland', 'Gujarat', 'Arunachal Pradesh', 'Tripura', 'Uttarakhand', 'Puducherry', 'Karnataka', 'Mizoram', 'Chattisgarh', 'Uttar Pradesh', 'Andaman and Nicobar Islands']
sl_no=0
for i in state:
    #row=[]
    #row=i.split(',')
    lat,lng=getll(i+",India")
    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state":i,"latitude":lat,"longitude":lng})
    sl_no+=1
    time.sleep(1)import scraperwiki
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
state=['Haryana', 'Punjab', 'Goa', 'Kerala', 'Dadra & Nagar Haveli', 'Jammu And Kashmir', 'Maharastra', 'Bihar', 'Assam', 'Chandigarh', 'Jharkhand', 'Meghalaya', 'Orissa', 'Daman & Diu', 'Madhya Pradesh', 'Lakshadweep', 'Manipur', 'Rajasthan', 'NCT of Delhi', 'Tamil Nadu', 'Sikkim', 'West Bengal', 'Andhra Pradesh', 'Himachal Pradesh', 'Nagaland', 'Gujarat', 'Arunachal Pradesh', 'Tripura', 'Uttarakhand', 'Puducherry', 'Karnataka', 'Mizoram', 'Chattisgarh', 'Uttar Pradesh', 'Andaman and Nicobar Islands']
sl_no=0
for i in state:
    #row=[]
    #row=i.split(',')
    lat,lng=getll(i+",India")
    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state":i,"latitude":lat,"longitude":lng})
    sl_no+=1
    time.sleep(1)