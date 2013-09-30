import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://daniels.du.edu/about/directory/")
root = lxml.html.fromstring(html)
for el in root.cssselect(".directory-name a"):
   name = el.text
   if name is not None:
       dat1= el.getparent()
       # dat= dat1.getnext()
       dat= dat1.getprevious()
       dat= dat1.getprevious()
       if dat.text is not None:
           print dat.text
       data = {
            'Name' : name,
             'Image URL' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

         
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://daniels.du.edu/about/directory/")
root = lxml.html.fromstring(html)
for el in root.cssselect(".directory-name a"):
   name = el.text
   if name is not None:
       dat1= el.getparent()
       # dat= dat1.getnext()
       dat= dat1.getprevious()
       dat= dat1.getprevious()
       if dat.text is not None:
           print dat.text
       data = {
            'Name' : name,
             'Image URL' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Name'], data=data)

         
