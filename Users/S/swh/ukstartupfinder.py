import scraperwiki

import scraperwiki

import lxml.html
import re
import urllib
from dateutil import parser

url = "http://readwrite.com/"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}



for story in root.cssselect('article'):

  try:
     content = story.cssselect('p')[0].text_content()
     if re.search(r"UK|enterprise|small business",content):
       print content
  except:
     print "fails"  
  



import scraperwiki

import scraperwiki

import lxml.html
import re
import urllib
from dateutil import parser

url = "http://readwrite.com/"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}



for story in root.cssselect('article'):

  try:
     content = story.cssselect('p')[0].text_content()
     if re.search(r"UK|enterprise|small business",content):
       print content
  except:
     print "fails"  
  



