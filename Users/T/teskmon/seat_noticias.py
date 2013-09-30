#!/usr/bin/env python

import scraperwiki
import lxml.html
import dateutil.parser

URL = 'http://seat-mediacenter.es/es-stories/proc'

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding="utf-8"))

for item in root.cssselect('div.griditem'):
    noticia = {
      'url' : URL + item.cssselect('a')[0].get('href'),
      'titulo' : item.cssselect('div.title')[0].text,
      'fecha' : dateutil.parser.parse(item.cssselect('div.date')[0].text, dayfirst=True).date(),
      'texto' : item.cssselect('div.subheadline')[0].text
    }
    scraperwiki.sqlite.save(['url'], noticia)
#!/usr/bin/env python

import scraperwiki
import lxml.html
import dateutil.parser

URL = 'http://seat-mediacenter.es/es-stories/proc'

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html, parser=lxml.html.HTMLParser(encoding="utf-8"))

for item in root.cssselect('div.griditem'):
    noticia = {
      'url' : URL + item.cssselect('a')[0].get('href'),
      'titulo' : item.cssselect('div.title')[0].text,
      'fecha' : dateutil.parser.parse(item.cssselect('div.date')[0].text, dayfirst=True).date(),
      'texto' : item.cssselect('div.subheadline')[0].text
    }
    scraperwiki.sqlite.save(['url'], noticia)
