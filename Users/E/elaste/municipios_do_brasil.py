# -*- coding: utf-8 -*-
import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki           
html = scraperwiki.scrape("http://www.ibge.gov.br/home/geociencias/areaterritorial/area.php?nome=a&codigo=&submit.x=46&submit.y=8")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='miolo_interno'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'Código UF' : tds[0].text_content(),
            'UF' : tds[1].text_content(),
            'Codigo Municipio' : tds[2].text_content(),
            'Municipio' : tds[3].text_content(),
            'Area' : tds[4].text_content()

        }
        scraperwiki.sqlite.save(unique_keys=['Codigo Municipio'], data=data)# -*- coding: utf-8 -*-
import scraperwiki

# Blank Python

print "Hello, coding in the cloud!"

import scraperwiki           
html = scraperwiki.scrape("http://www.ibge.gov.br/home/geociencias/areaterritorial/area.php?nome=a&codigo=&submit.x=46&submit.y=8")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[id='miolo_interno'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'Código UF' : tds[0].text_content(),
            'UF' : tds[1].text_content(),
            'Codigo Municipio' : tds[2].text_content(),
            'Municipio' : tds[3].text_content(),
            'Area' : tds[4].text_content()

        }
        scraperwiki.sqlite.save(unique_keys=['Codigo Municipio'], data=data)