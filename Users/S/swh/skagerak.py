import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.skagerakgroup.com/en-US/News.aspx"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('div.news-item'):
  stories['date'] = parser.parse(story.cssselect('span.date')[0].text)
  stories['summary'] = story.cssselect('p')[0].text
  stories['link'] = "http://www.skagerakgroup.com/" + story.cssselect('a')[0].attrib['href']
  stories['title'] = story.cssselect('a')[0].cssselect('h3')[0].text
  scraperwiki.sqlite.save(['link'],stories)
  

  
