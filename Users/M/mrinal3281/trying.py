import scraperwiki
import urllib
import csv
import string

from geopy import geocoders 
g = geocoders.Google(domain='maps.google.co.in')
#data=data = scraperwiki.scrape("C:\\Documents and Settings\\ignite192\\My Documents\\Downloads\\mrinal_14.csv")

#reader = csv.reader(data.splitlines())
#for row in reader: print "£%s spent on %s" % (row[7], row[3])

scraperwiki.sqlite.attach("Daman & Diu", "src1") 
lis= scraperwiki.sqlite.select("village_name from src1.swdata")
lis2=scraperwiki.sqlite.select("Sub_district_Name from src1.swdata")
lis3=scraperwiki.sqlite.select("District_Name from src1.swdata")
i=0
#print lis[1]
#for i in range(100):
#    st=lis3[i]['District_Name']
#    print st
#    st1=lis2[i]['Sub_district_Name']
#    print st1
#    st2=lis[i]['village_name']
#    print st2
#    place,(lat,lng) = g.geocode(st+"bihar")
#    print(place,lat,lng)
place,(lat,lng) = g.geocode(lis3[1]['District_Name']+"bihar")
print(lat,lng)
import scraperwiki
import urllib
import csv
import string

from geopy import geocoders 
g = geocoders.Google(domain='maps.google.co.in')
#data=data = scraperwiki.scrape("C:\\Documents and Settings\\ignite192\\My Documents\\Downloads\\mrinal_14.csv")

#reader = csv.reader(data.splitlines())
#for row in reader: print "£%s spent on %s" % (row[7], row[3])

scraperwiki.sqlite.attach("Daman & Diu", "src1") 
lis= scraperwiki.sqlite.select("village_name from src1.swdata")
lis2=scraperwiki.sqlite.select("Sub_district_Name from src1.swdata")
lis3=scraperwiki.sqlite.select("District_Name from src1.swdata")
i=0
#print lis[1]
#for i in range(100):
#    st=lis3[i]['District_Name']
#    print st
#    st1=lis2[i]['Sub_district_Name']
#    print st1
#    st2=lis[i]['village_name']
#    print st2
#    place,(lat,lng) = g.geocode(st+"bihar")
#    print(place,lat,lng)
place,(lat,lng) = g.geocode(lis3[1]['District_Name']+"bihar")
print(lat,lng)
