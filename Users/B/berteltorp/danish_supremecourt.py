import scraperwiki
# import requests
import lxml.html
import time
# import re

import feedparser
feed = feedparser.parse('http://www.domstol.dk/_layouts/feed.aspx?xsl=1&web=%2Fhojesteret%2FEU%2Dret&page=d43cc549-a975-45ba-824c-e8c1ec62b31e&wp=77b06ce9-cf41-44be-b39d-6059a2cd3d0d')
for dom in feed.entries:
#  print dom.keys()
  beskrivelse = dom.title
  popnavn = dom.description
  afsagt = dom.updated
  domurl = dom.link
  htmltree = lxml.html.parse(dom.link)
  p_tags = htmltree.xpath('//p')
  p_content = [p.text_content() for p in p_tags]
  domstekst = ' '.join(p_content)
  data = {
            'popnavn' : popnavn,
            'beskrivelse' : beskrivelse,
            'afsagt' : afsagt,
            'domurl' : domurl,
            'beskrivelse' : beskrivelse,
            'domstekst' : domstekst
        }
  scraperwiki.sqlite.save(unique_keys=['popnavn'], data=data)