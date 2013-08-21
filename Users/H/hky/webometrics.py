#!/usr/bin/env python

import scraperwiki
import lxml.html
import urllib
for u in range (0, 20400, 50):
    url = 'http://www.webometrics.info/top12000.asp?offset=%s' % u
    #html = scraperwiki.scrape(url)
    # more tolerant HTTP header parser to fix BadStatusLine
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr.nav6a"):
        tds = tr.cssselect("td")
        data = {
          'world_rank' : int(tds[0].text_content().replace(',', '')),
          'university' : tds[1].text_content().strip(),
          'size' : int(tds[3].text_content().replace(',', '')),
          'visibility' : int(tds[4].text_content().replace(',', '')),
          'rich_files' : int(tds[5].text_content().replace(',', '')),
          'scholar' : int(tds[6].text_content().replace(',', ''))
        }
        scraperwiki.sqlite.save(unique_keys=['world_rank'], data=data)
