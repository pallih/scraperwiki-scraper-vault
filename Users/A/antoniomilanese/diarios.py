import scraperwiki

# Blank Python

import scraperwiki           
html = scraperwiki.scrape("http://buscar.lanacion.com.ar/corrupcion")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'data' : tds[0].text_content(), 
        }
        scraperwiki.sqlite.save(unique_keys=['data'], data=data)
import scraperwiki

# Blank Python

import scraperwiki           
html = scraperwiki.scrape("http://buscar.lanacion.com.ar/corrupcion")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'data' : tds[0].text_content(), 
        }
        scraperwiki.sqlite.save(unique_keys=['data'], data=data)
