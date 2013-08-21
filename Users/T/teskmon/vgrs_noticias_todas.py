#!/usr/bin/env python

import scraperwiki
import lxml.html
import dateutil.parser

URL = 'http://www.vwgroupretail.es/inicio/noticias'

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding="utf-8"))

for item in root.cssselect('div.cell'):
    noticia = {
      'url' : URL + item.cssselect('a.theme')[0].get('href'),
      'titulo' : item.cssselect('a.theme')[0].text,
      'fecha' : dateutil.parser.parse(item.cssselect('li.date')[0].text, dayfirst=True).date(),
      'texto' : item.cssselect('li.article')[0].text
    }
    scraperwiki.sqlite.save(['url'], noticia)
