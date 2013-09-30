import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import urllib2
import re
import math

scraperwiki.sqlite.attach('books-hs18-category-url','url')
list_urls = scraperwiki.sqlite.select('* from url.swdata')
print 'length :'+str(len(list_urls))
print type(list_urls)

count=0
print type(count)

for urls in list_urls:
 data = {}
 categories = urls.values()
 url = categories[0]
 category = categories[1]
 count = count+1
 print count

 print category
 print url
 
 open = urllib2.urlopen(url)
 lines = str(open.readlines())
 match_noofproducts = re.search(r'(orange_highlight">[\w\s\d&-]+</span>\s+\()(\d+)(\))',lines)
 if match_noofproducts:
  noofproducts = match_noofproducts.group(2)
  print type(noofproducts)
  noofpages = float(noofproducts)/24.0
  noofpages = int(math.ceil(noofpages))
  print noofpages
  match_sampleurl = re.search(r'(http://www.homeshop18.com/[\w\d-]+/categoryid:\d+/search:/listView:true/start:\d+/)(\'>\d+)',lines)
  if match_sampleurl:
   url =  match_sampleurl.group(1)
  url.replace("start:\d+","start:7777777")
  sampleurl = url[:-3]
  for pageno in range(noofpages):
   resultpage_url = sampleurl+str(pageno*24)
   print 'result page : '+resultpage_url
   print category
   scraperwiki.sqlite.save(['url'],data={'url':resultpage_url,'category':category})

import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import urllib2
import re
import math

scraperwiki.sqlite.attach('books-hs18-category-url','url')
list_urls = scraperwiki.sqlite.select('* from url.swdata')
print 'length :'+str(len(list_urls))
print type(list_urls)

count=0
print type(count)

for urls in list_urls:
 data = {}
 categories = urls.values()
 url = categories[0]
 category = categories[1]
 count = count+1
 print count

 print category
 print url
 
 open = urllib2.urlopen(url)
 lines = str(open.readlines())
 match_noofproducts = re.search(r'(orange_highlight">[\w\s\d&-]+</span>\s+\()(\d+)(\))',lines)
 if match_noofproducts:
  noofproducts = match_noofproducts.group(2)
  print type(noofproducts)
  noofpages = float(noofproducts)/24.0
  noofpages = int(math.ceil(noofpages))
  print noofpages
  match_sampleurl = re.search(r'(http://www.homeshop18.com/[\w\d-]+/categoryid:\d+/search:/listView:true/start:\d+/)(\'>\d+)',lines)
  if match_sampleurl:
   url =  match_sampleurl.group(1)
  url.replace("start:\d+","start:7777777")
  sampleurl = url[:-3]
  for pageno in range(noofpages):
   resultpage_url = sampleurl+str(pageno*24)
   print 'result page : '+resultpage_url
   print category
   scraperwiki.sqlite.save(['url'],data={'url':resultpage_url,'category':category})

