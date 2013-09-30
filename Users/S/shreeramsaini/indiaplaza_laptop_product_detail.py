import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('indiaplaza_laptop_product_url','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

for dict_urls in list_urls:
 url = dict_urls['url']
 open = urllib2.urlopen(url)
 page = str(open.readlines())
 openlines = urllib2.urlopen(url)
 lines = openlines.readlines()
 
 print url  
 price=0

 match_title = re.search(r'(<span.{0,50}lblTitle.{0,10}">)([\w\s\d]+)',page)
 if match_title:
    title = match_title.group(2)
   
 match_price = re.search(r'(<span id="lblOurPrice" class="price_fdp">)([\d\.]+)',page)
 if match_price:
  price = match_price.group(2)
  

 match_delivery = re.search(r'(delDateQuest.{0,3}>[\w\s]+)(\d+)',page)
 if match_delivery:
  delivery = match_delivery.group(2)  
 
 scraperwiki.sqlite.save(['url'],data={'url':url,'title':title,'price':price,'delivery':delivery,'shipping':'Free','stock':'In'})import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('indiaplaza_laptop_product_url','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

for dict_urls in list_urls:
 url = dict_urls['url']
 open = urllib2.urlopen(url)
 page = str(open.readlines())
 openlines = urllib2.urlopen(url)
 lines = openlines.readlines()
 
 print url  
 price=0

 match_title = re.search(r'(<span.{0,50}lblTitle.{0,10}">)([\w\s\d]+)',page)
 if match_title:
    title = match_title.group(2)
   
 match_price = re.search(r'(<span id="lblOurPrice" class="price_fdp">)([\d\.]+)',page)
 if match_price:
  price = match_price.group(2)
  

 match_delivery = re.search(r'(delDateQuest.{0,3}>[\w\s]+)(\d+)',page)
 if match_delivery:
  delivery = match_delivery.group(2)  
 
 scraperwiki.sqlite.save(['url'],data={'url':url,'title':title,'price':price,'delivery':delivery,'shipping':'Free','stock':'In'})