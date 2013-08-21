#!/usr/bin/env python

import scraperwiki
import lxml.html
import urllib

for u in range (0, 4):
    #url = 'http://www.webometrics.info/rank_by_country.asp?country=id&offset=%s' % u
    url = 'http://www.webometrics.info/en/Asia/Indonesia?page=%s' %u
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

