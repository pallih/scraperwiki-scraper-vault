import scraperwiki
# import requests
import lxml.html
# import time
# import re

import feedparser
feed = feedparser.parse('http://www.domstol.dk/_layouts/feed.aspx?xsl=1&web=%2Fhojesteret%2Fnyheder%2FAfgorelser&page=cfc30285-ca31-4ccf-837d-6d98e716505f&wp=b1d48020-4cef-4704-b53a-33dcbb9e60e1')
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
# import time
# import re

import feedparser
feed = feedparser.parse('http://www.domstol.dk/_layouts/feed.aspx?xsl=1&web=%2Fhojesteret%2Fnyheder%2FAfgorelser&page=cfc30285-ca31-4ccf-837d-6d98e716505f&wp=b1d48020-4cef-4704-b53a-33dcbb9e60e1')
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