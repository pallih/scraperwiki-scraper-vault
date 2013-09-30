import scraperwiki
import lxml.html
# Blank Python
import datetime
import dateutil.parser

html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue/maps.html")

root = lxml.html.fromstring(html)
for el in root.cssselect("td a"):
   coun = el.text
   print coun
  for k in root.cssselect("td br"):
   Date = k.text
  print k.text
  #scraperwiki.sqlite.save(unique_keys=['country'], data=data)
if coun is not None:
          data = {
            'country' :coun
      
                }
           
#data = {'country' :coun,}
scraperwiki.sqlite.save(unique_keys=['country'], data=data)  
 
print html


import scraperwiki
import lxml.html
# Blank Python
import datetime
import dateutil.parser

html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue/maps.html")

root = lxml.html.fromstring(html)
for el in root.cssselect("td a"):
   coun = el.text
   print coun
  for k in root.cssselect("td br"):
   Date = k.text
  print k.text
  #scraperwiki.sqlite.save(unique_keys=['country'], data=data)
if coun is not None:
          data = {
            'country' :coun
      
                }
           
#data = {'country' :coun,}
scraperwiki.sqlite.save(unique_keys=['country'], data=data)  
 
print html


