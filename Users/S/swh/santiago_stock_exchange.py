import scraperwiki

import lxml.html
import re
import urllib
from dateutil import parser

url = "http://www.bolsadesantiago.com/Theme/noticiasBS.aspx"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}
companies = ["la", "Multiexport Foods", "Aquachile"]

for story in root.cssselect('tr.bcs-portlet-section-body'):
  date = parser.parse(story.cssselect('td')[0].cssselect('a')[0].text)
  title = story.cssselect('td')[1].cssselect('a')[0].text
  link = "http://www.bolsadesantiago.com/Theme/" + story.cssselect('td')[0].cssselect('a')[0].attrib['href']
  for company in companies:
    if re.search(company,title):
      stories['title'] = title
      stories['date'] = date
      stories['link'] = link
      stories['company'] = company
      scraperwiki.sqlite.save(['link'],stories)


import scraperwiki

import lxml.html
import re
import urllib
from dateutil import parser

url = "http://www.bolsadesantiago.com/Theme/noticiasBS.aspx"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}
companies = ["la", "Multiexport Foods", "Aquachile"]

for story in root.cssselect('tr.bcs-portlet-section-body'):
  date = parser.parse(story.cssselect('td')[0].cssselect('a')[0].text)
  title = story.cssselect('td')[1].cssselect('a')[0].text
  link = "http://www.bolsadesantiago.com/Theme/" + story.cssselect('td')[0].cssselect('a')[0].attrib['href']
  for company in companies:
    if re.search(company,title):
      stories['title'] = title
      stories['date'] = date
      stories['link'] = link
      stories['company'] = company
      scraperwiki.sqlite.save(['link'],stories)


