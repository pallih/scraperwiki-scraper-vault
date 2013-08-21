#!/usr/bin/env python

import scraperwiki
import lxml.html
import dateutil.parser

URL = 'http://prensa.audi.es/'

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding="utf-8"))

for item in root.cssselect('ul.noticias li[class~="actual"]'):
    id = item.get('id')
    titulo = item.cssselect('h3 a')[0]
    fecha = item.cssselect('p.fecha')[0].text
    noticia = {
      'id' : int(id[id.find("-")+1:]),
      'url' : titulo.get('href'),
      'titulo' : titulo.text,
      'fecha' : dateutil.parser.parse(fecha, dayfirst=True).date(),
      'texto' : item.cssselect('p.fecha + p + p')[0].text
    }
    scraperwiki.sqlite.save(['id'], noticia)
