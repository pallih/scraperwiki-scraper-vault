import scraperwiki
# import requests
import lxml.html
# import time
# import re

import feedparser
feed = feedparser.parse('http://ekstrabladet.dk/rss2/?mode=normal&submode=nyheder')
for artikel in feed.entries:
#  print artikel.keys()
  overskrift = artikel.title
  kategori = artikel.tags
  dato = artikel.updated
  link = artikel.link
  htmltree = lxml.html.parse(artikel.link)
  p_tags = htmltree.xpath('//div[@class=bodytext]')
  p_content = [p.text_content() for p in p_tags]
  tekst = ' '.join(p_content)
  data = {
            'overskrift' : overskrift,
            'kategori' : kategori,
            'dato' : dato,
            'link' : link,
            'tekst' : tekst
        }
  scraperwiki.sqlite.save(unique_keys=['overskrift'], data=data)