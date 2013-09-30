import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.uwyo.edu/geolgeophys/people/")
root = lxml.html.fromstring(html)
for el in root.cssselect("#bodycopy tbody tr td a"):
   people = el.text
   print el
   print el.text
   if people is not None:
       dat= el.getparent()
       #dat2= dat1.getnext()
       #dat= dat2.getnext()
       if dat.text is not None:
           print dat2.text
       data = {
              'people' : people,
              'title' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['people'], data=data)

         
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.uwyo.edu/geolgeophys/people/")
root = lxml.html.fromstring(html)
for el in root.cssselect("#bodycopy tbody tr td a"):
   people = el.text
   print el
   print el.text
   if people is not None:
       dat= el.getparent()
       #dat2= dat1.getnext()
       #dat= dat2.getnext()
       if dat.text is not None:
           print dat2.text
       data = {
              'people' : people,
              'title' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['people'], data=data)

         
