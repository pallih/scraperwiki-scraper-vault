import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.uwyo.edu/geolgeophys/people/graduate-students.html")
root = lxml.html.fromstring(html)
for el in root.cssselect("#bodycopy tbody tr td a"):
   people = el.text
   print el
   print el.text
   if people is not None:
       dat1= el.getparent()
       dat= dat1.getnext()
       if dat1.text is not None:
           print dat1.text
       data = {
              'people' : people,
              'title' : dat1.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['people'], data=data)

         
