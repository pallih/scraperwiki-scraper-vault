import scraperwiki

# Blank Python

import re
import urllib2

url = "http://www.homeshop18.com/laptops/categoryid:3291/search:*/sort:Best+Sellers/start:48/inStock:true/"
#http://www.homeshop18.com/hp-2000-2202tu-intel-core-i3-2gb-500gb-windows-8-15-6-laptop/computer-peripherals/laptops/product:30386214/cid:3291/?pos=49

page = urllib2.urlopen(url)
lines  = page.readlines()
pagefull = str(lines)

count = 1
for line in lines:
  match_product_url = re.search(r'http://www.homeshop18.com.*computer-peripherals/laptops/product:\d+/cid:\d+',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1
