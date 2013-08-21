import scraperwiki

# Blank Python

import lxml.html
import datetime
import dateutil.parser
html = scraperwiki.scrape("http://www.mapaction.org/map-catalogue/maps.html?deployment_filter=216")
root = lxml.html.fromstring(html)
for el in root.cssselect("tr td a"):
#for el in root.cssselect("h2 a"):
 coun = el.text
 print coun
if coun is not None:
          data1 = {
          "country" :el.text
                 }

scraperwiki.sqlite.save(unique_keys=["country"],data=data1)

#scraperwiki.sqlite.save("country", coun)
scraperwiki.datastore.save(["country"], data=data1)