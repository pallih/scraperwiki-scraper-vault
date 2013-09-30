import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
print html

#for el in root.cssselect("div.featured a"):
   ###print el.attrib['href']
el = root.cssselect("div#nav")[0]
    #print el
print el.text