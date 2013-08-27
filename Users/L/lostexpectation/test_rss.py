import scraperwiki
import lxml.html, lxml.cssselect
import re

rssurl="http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"

# load
root = lxml.html.parse(rssurl).getroot()


#parse
for item in root.cssselect('rss > channel > item'):
  d1 = (item.cssselect('title')[0]).text
  d2  = (item.cssselect('link')[0]).text
  d3  = (item.cssselect('ol')[0]).text
  # new record
  record = {}
  record['title'] = d1
  record['link'] = d2
  record['desc'] = d3
  # parse more
  
scraperwiki.datastore.save(unique_keys=['title'], data=record)import scraperwiki
import lxml.html, lxml.cssselect
import re

rssurl="http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"

# load
root = lxml.html.parse(rssurl).getroot()


#parse
for item in root.cssselect('rss > channel > item'):
  d1 = (item.cssselect('title')[0]).text
  d2  = (item.cssselect('link')[0]).text
  d3  = (item.cssselect('ol')[0]).text
  # new record
  record = {}
  record['title'] = d1
  record['link'] = d2
  record['desc'] = d3
  # parse more
  
scraperwiki.datastore.save(unique_keys=['title'], data=record)import scraperwiki
import lxml.html, lxml.cssselect
import re

rssurl="http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml"

# load
root = lxml.html.parse(rssurl).getroot()


#parse
for item in root.cssselect('rss > channel > item'):
  d1 = (item.cssselect('title')[0]).text
  d2  = (item.cssselect('link')[0]).text
  d3  = (item.cssselect('ol')[0]).text
  # new record
  record = {}
  record['title'] = d1
  record['link'] = d2
  record['desc'] = d3
  # parse more
  
scraperwiki.datastore.save(unique_keys=['title'], data=record)