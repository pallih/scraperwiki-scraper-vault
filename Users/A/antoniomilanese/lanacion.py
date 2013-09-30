import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://buscar.lanacion.com.ar/corrupcion/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.data"):
    print el
print lxml.html.tostring(el)
import scraperwiki

# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://buscar.lanacion.com.ar/corrupcion/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.data"):
    print el
print lxml.html.tostring(el)
