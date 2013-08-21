import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.reuters.com/finance/stocks/SELr.AT/key-developments"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('div.feature'):
  headline = story.cssselect('h2')[0]
  stories['title'] = headline.cssselect('a')[0].text
  stories['link'] = "http://www.reuters.com/" + headline.cssselect('a')[0].attrib['href']
  stories['date'] = parser.parse(story.cssselect('span.timestamp')[0].text)
  stories['summary'] = story.cssselect('p')[0].text
  scraperwiki.sqlite.save(['link'],stories)
  
 
  

