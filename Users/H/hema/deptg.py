import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.uwyo.edu/geolgeophys/people/")
root = lxml.html.fromstring(html)
for el in root.cssselect("#bodycopy tbody tr td a "):
   people = el.text
   print el
   print "HHHHHHHHHHHHHH"
   print el.text
   print el.getnext()
   if people is not None:
       dat= el.getparent()
       dat1= el.getnext()
       #dat1= dat2.getnext()
       if dat.text is not None:
          print dat1.text
          print dat.text
       data = {
              'people' : people,
              'title' : el.getnext()
               }
       print data
       scraperwiki.sqlite.save(unique_keys=['people'], data=data)

         