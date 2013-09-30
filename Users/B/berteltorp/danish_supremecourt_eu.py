import scraperwiki
# import requests
import lxml.html
#import time
# import re

import feedparser
feed = feedparser.parse('http://www.domstol.dk/_layouts/feed.aspx?xsl=1&web=%2Fhojesteret%2FEMRK&page=d2e34683-c67e-475d-b652-92c3e3db3c30&wp=936911fc-1818-437f-8d5f-315d4699bb1c')
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
  scraperwiki.sqlite.save(unique_keys=['popnavn'], data=data)import scraperwiki
# import requests
import lxml.html
#import time
# import re

import feedparser
feed = feedparser.parse('http://www.domstol.dk/_layouts/feed.aspx?xsl=1&web=%2Fhojesteret%2FEMRK&page=d2e34683-c67e-475d-b652-92c3e3db3c30&wp=936911fc-1818-437f-8d5f-315d4699bb1c')
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