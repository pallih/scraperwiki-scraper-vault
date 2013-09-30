import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.espersen.dk/?Id=955"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('div.rightcol p'):
  
  stories['title'] = story.cssselect('a')[0].text_content()[12:]
  stories['link'] = "http://www.espersen.dk/" + story.cssselect('a')[0].attrib['href']
  stories['date'] = parser.parse(story.cssselect('a')[0].text_content()[:10])
  scraperwiki.sqlite.save(['link'],stories) 
import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.espersen.dk/?Id=955"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('div.rightcol p'):
  
  stories['title'] = story.cssselect('a')[0].text_content()[12:]
  stories['link'] = "http://www.espersen.dk/" + story.cssselect('a')[0].attrib['href']
  stories['date'] = parser.parse(story.cssselect('a')[0].text_content()[:10])
  scraperwiki.sqlite.save(['link'],stories) 
