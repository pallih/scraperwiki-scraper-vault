import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/index.shtml")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"):
   coun = el.text
   if coun is not None:
       dat1= el.getparent()
       dat= dat1.getnext()
       if dat.text is not None:
           print dat.text
       data = {
            'Country' : coun,
             'Date' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.un.org/en/members/index.shtml")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.countryname a"):
   coun = el.text
   if coun is not None:
       dat1= el.getparent()
       dat= dat1.getnext()
       if dat.text is not None:
           print dat.text
       data = {
            'Country' : coun,
             'Date' : dat.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
