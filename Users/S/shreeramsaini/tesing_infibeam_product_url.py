import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('infibeam_laptop_page_url','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

count = 1
for dict_urls in list_urls:
 url = dict_urls['url']
 print url
 
 open = urllib2.urlopen(url)
 page = str(open.readlines()) 

 matches = re.findall(r'(href=")(/Laptop/[./?=\w\d-]+)',page)
 for match in matches: 
  pagelink = 'http://www.infibeam.com'+match[1]
  print pagelink
 
  scraperwiki.sqlite.save(['url'],data={'url':pagelink})
  print count 
  count = count + 1
  #print "Repeat "+pagelink


                   
import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('infibeam_laptop_page_url','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

count = 1
for dict_urls in list_urls:
 url = dict_urls['url']
 print url
 
 open = urllib2.urlopen(url)
 page = str(open.readlines()) 

 matches = re.findall(r'(href=")(/Laptop/[./?=\w\d-]+)',page)
 for match in matches: 
  pagelink = 'http://www.infibeam.com'+match[1]
  print pagelink
 
  scraperwiki.sqlite.save(['url'],data={'url':pagelink})
  print count 
  count = count + 1
  #print "Repeat "+pagelink


                   
