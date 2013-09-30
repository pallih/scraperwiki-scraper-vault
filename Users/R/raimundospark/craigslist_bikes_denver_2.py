import scraperwiki
import lxml.html
# Blank Python

#Craigslist
html = scraperwiki.scrape("http://denver.craigslist.org/bia/")
root = lxml.html.fromstring(html)
data = {}
line = []
c=0
#Entries
for el in root.cssselect("p.row"):
    price = el.cssselect("span.itempp")[0].text_content()
    loc = el.cssselect("span.itempn")[0].text_content()
    link_text = el.cssselect("a")[0].text_content()
    link = el.cssselect("a")[0].attrib['href']
    print link_text,price,loc,linkimport scraperwiki
import lxml.html
# Blank Python

#Craigslist
html = scraperwiki.scrape("http://denver.craigslist.org/bia/")
root = lxml.html.fromstring(html)
data = {}
line = []
c=0
#Entries
for el in root.cssselect("p.row"):
    price = el.cssselect("span.itempp")[0].text_content()
    loc = el.cssselect("span.itempn")[0].text_content()
    link_text = el.cssselect("a")[0].text_content()
    link = el.cssselect("a")[0].attrib['href']
    print link_text,price,loc,link