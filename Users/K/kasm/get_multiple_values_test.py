import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://rhizome.org/supporters/")
root = lxml.html.fromstring(html)
for el in root.cssselect(".support-level"):
   level = el.text
   print el
   print el.text
   if level is not None:
       #dat1= el.getparent()
       sup= el.getnext()
       if sup.text is not None:
           print sup.text
       data = {
            'Level' : level,
             'Supporters' : sup.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Supporters'], data=data)
