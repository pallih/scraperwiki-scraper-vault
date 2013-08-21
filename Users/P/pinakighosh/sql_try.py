import scraperwiki
from geopy import geocoders  

def getll(loc):
    g = geocoders.Google(domain='maps.google.co.uk')
    try:
        for place, (lat, lng) in g.geocode(loc,exactly_one=False):
            #print "%s: %.5f, %.5f" % (place, lat, lng)
            ltd=lat
            lngt=lng
    except:
        ltd=0
        lngt=0
    return ltd,lngt
scraperwiki.sqlite.attach("village_7","data")
#print scraperwiki.sqlite.select("* Pinaki Ghosh / village_7.swdata limit 2")
s=scraperwiki.sqlite.select("village_name,District_Name,Sub_district_Name from data.swdata where sl_no<10") #return a list of dictionary
for i in range(len(s)):
    loc=""
    for j in s[i]:
        loc=loc+","+s[i][j]
    loc=loc+",India"
    print loc

print "completed"


