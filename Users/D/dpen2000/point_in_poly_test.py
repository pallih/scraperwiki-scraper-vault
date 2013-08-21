import scraperwiki
from array import *
import re
from lxml import etree
# Blank Python

def point_in_poly(x,y,poly):

   # check if point is a vertex
   if (x,y) in poly: return "IN"

   # check if point is on a boundary
   for i in range(len(poly)):
      p1 = None
      p2 = None
      if i==0:
         p1 = poly[0]
         p2 = poly[1]
      else:
         p1 = poly[i-1]
         p2 = poly[i]
      if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
         return "IN"
      
   n = len(poly)
   inside = False

   p1x,p1y = poly[0]
   for i in range(n+1):
      p2x,p2y = poly[i % n]
      if y > min(p1y,p2y):
         if y <= max(p1y,p2y):
            if x <= max(p1x,p2x):
               if p1y != p2y:
                  xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

   if inside: return "IN"
   else: return "OUT"




poly2 = [(1,1), (5,1), (5,5), (1,5), (1,1)]
x = 10
y = 30
print point_in_poly(x, y, poly2)

#scraperwiki.sqlite.attach("tate_liverpool_exhibitions_data", "zarino")
#data = scraperwiki.sqlite.select("postcode_district, avg(lat) as LatAverage, avg(long) as LongAverage, count(postcode) as Visits from zarino.swdata where lat is not null group by postcode_district")
#for row in data:
#    postcode = row["postcode_district"]
#    result = re.search("([A-Z]+)?([0-9]+)", postcode)
#    if result:
#        row["postcode_district_letter"] = result.group(1)
#        row["postcode_district_number"] = result.group(2)
#        scraperwiki.sqlite.save(unique_keys=["postcode_district"], data=row)

kml = scraperwiki.scrape('http://dl.dropbox.com/u/15570665/exporttable.kml')
root = etree.fromstring(kml)
print root.find("kml").tag

