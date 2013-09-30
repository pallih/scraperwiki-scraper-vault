import scraperwiki

import urllib2
import re

url = "http://www.homeshop18.com/desktops/category:3286/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

count = 1
for line in lines:
 match_product_url = re.search(r'http://www.homeshop18.com.*computer-peripherals/desktops/product:\d+/cid:\d+',str(line))
 if match_product_url:
   purl = match_product_url.group()
   scraperwiki.sqlite.save(['url'],data={'url':purl})
   print count
   count = count + 1

import scraperwiki

import urllib2
import re

url = "http://www.homeshop18.com/desktops/category:3286/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

count = 1
for line in lines:
 match_product_url = re.search(r'http://www.homeshop18.com.*computer-peripherals/desktops/product:\d+/cid:\d+',str(line))
 if match_product_url:
   purl = match_product_url.group()
   scraperwiki.sqlite.save(['url'],data={'url':purl})
   print count
   count = count + 1

