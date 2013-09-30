import scraperwiki
#Blank Python
import scraperwiki
import lxml.html

import datetime
import dateutil.parser

html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue.html")

root = lxml.html.fromstring(html)
for el in root.cssselect("h2 a"):
   coun = el.text
   print coun
   for k in root.cssselect("br"):
    Date = k.text
   print k.text
  
if coun is not None:
          data = {
            'country' :coun
      
                }
           
scraperwiki.sqlite.save(unique_keys=['country'], data=data)  
 
print html


import scraperwiki
#Blank Python
import scraperwiki
import lxml.html

import datetime
import dateutil.parser

html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue.html")

root = lxml.html.fromstring(html)
for el in root.cssselect("h2 a"):
   coun = el.text
   print coun
   for k in root.cssselect("br"):
    Date = k.text
   print k.text
  
if coun is not None:
          data = {
            'country' :coun
      
                }
           
scraperwiki.sqlite.save(unique_keys=['country'], data=data)  
 
print html


