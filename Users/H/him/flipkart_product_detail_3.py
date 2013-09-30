import scraperwiki

import re
import urllib2
url = "http://www.flipkart.com/unix-concepts-applications-3-e-3rd/p/itmczyntg5agaca9?pid=9780070534759&query=9780070534759"
 
ProductPage = urllib2.urlopen(url)
lines = ProductPage.readlines()
 
for line in lines:
   match_title = re.search(r'<h1.*title="(.*)"',str(line))
   if match_title:
    title = match_title.group(1)
    print title

   match_price = re.search(r'final-price">.{0,100}Rs\.[\s]+([\d]+)',str(line))
   if match_price:
    price = match_price.group(1)
    print price

   match_stock = re.search(r'fk-stock-info-id.{0,5}>(\w+)',str(line))
   if match_stock:
    stock = match_stock.group(1)
    print stock

   match_delivery = re.search(r'([\d\s]+-[\d]+)\s+business\s+days',str(line))
   if match_delivery:
    delivery = match_delivery.group(1)
    print delivery

   match_shipping = re.search(r'FREE\s+Home\s+Delivery',str(line))
   if match_shipping:
    shipping = "Free"
    print shipping
  
import scraperwiki

import re
import urllib2
url = "http://www.flipkart.com/unix-concepts-applications-3-e-3rd/p/itmczyntg5agaca9?pid=9780070534759&query=9780070534759"
 
ProductPage = urllib2.urlopen(url)
lines = ProductPage.readlines()
 
for line in lines:
   match_title = re.search(r'<h1.*title="(.*)"',str(line))
   if match_title:
    title = match_title.group(1)
    print title

   match_price = re.search(r'final-price">.{0,100}Rs\.[\s]+([\d]+)',str(line))
   if match_price:
    price = match_price.group(1)
    print price

   match_stock = re.search(r'fk-stock-info-id.{0,5}>(\w+)',str(line))
   if match_stock:
    stock = match_stock.group(1)
    print stock

   match_delivery = re.search(r'([\d\s]+-[\d]+)\s+business\s+days',str(line))
   if match_delivery:
    delivery = match_delivery.group(1)
    print delivery

   match_shipping = re.search(r'FREE\s+Home\s+Delivery',str(line))
   if match_shipping:
    shipping = "Free"
    print shipping
  
import scraperwiki

import re
import urllib2
url = "http://www.flipkart.com/unix-concepts-applications-3-e-3rd/p/itmczyntg5agaca9?pid=9780070534759&query=9780070534759"
 
ProductPage = urllib2.urlopen(url)
lines = ProductPage.readlines()
 
for line in lines:
   match_title = re.search(r'<h1.*title="(.*)"',str(line))
   if match_title:
    title = match_title.group(1)
    print title

   match_price = re.search(r'final-price">.{0,100}Rs\.[\s]+([\d]+)',str(line))
   if match_price:
    price = match_price.group(1)
    print price

   match_stock = re.search(r'fk-stock-info-id.{0,5}>(\w+)',str(line))
   if match_stock:
    stock = match_stock.group(1)
    print stock

   match_delivery = re.search(r'([\d\s]+-[\d]+)\s+business\s+days',str(line))
   if match_delivery:
    delivery = match_delivery.group(1)
    print delivery

   match_shipping = re.search(r'FREE\s+Home\s+Delivery',str(line))
   if match_shipping:
    shipping = "Free"
    print shipping
  
