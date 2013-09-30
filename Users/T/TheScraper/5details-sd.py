import scraperwiki

# Blank Python

import re
import urllib2

regex_title = "r'h1'"
url = "http://www.snapdeal.com/product/apple-macbook-pro-13-inch/199160?pos=0;8"
pageopen = urllib2.urlopen(url)

lines = pageopen.readlines()
pagefull = str(lines)
print pagefull

for line in lines:
  #print line

  match_title = re.search(r'<h1 itemprop="name">[\w\s\(\)\d/]+',str(line))
  if match_title:
    print match_title.group()

  match_price = re.search(r'(Rs.{0,100}selling.{0,100}">)(\d+)',str(line))
  if match_price:
    print match_price.group(2)

  match_delivery = re.search(r'(Dispatched.{10,50}<strong>)([\w\s\d]+)</strong>',str(line))
  if match_delivery:
    print match_delivery.group(2)

match_shipping = re.search(r'(Shipping.{0,100}<span>)(\w+)(</span>)',pagefull)
if match_shipping:
  print match_shipping.group(2)



#<h1 itemprop="name">Apple MacBook Pro 13 inch (MD101HN/A)</h1>
#<strong class="redText">Rs <span id="selling-price-id">79999</span></strong>
#<div class="product-free-ship-outer">
#                                                <strong>Shipping Charges</strong>:
#                                                        <span>Free</span>
#                                            </div>
#<strong>5 business days </strong>
#<span><strong>Dispatched</strong> in <strong>3 business days </strong></span>
import scraperwiki

# Blank Python

import re
import urllib2

regex_title = "r'h1'"
url = "http://www.snapdeal.com/product/apple-macbook-pro-13-inch/199160?pos=0;8"
pageopen = urllib2.urlopen(url)

lines = pageopen.readlines()
pagefull = str(lines)
print pagefull

for line in lines:
  #print line

  match_title = re.search(r'<h1 itemprop="name">[\w\s\(\)\d/]+',str(line))
  if match_title:
    print match_title.group()

  match_price = re.search(r'(Rs.{0,100}selling.{0,100}">)(\d+)',str(line))
  if match_price:
    print match_price.group(2)

  match_delivery = re.search(r'(Dispatched.{10,50}<strong>)([\w\s\d]+)</strong>',str(line))
  if match_delivery:
    print match_delivery.group(2)

match_shipping = re.search(r'(Shipping.{0,100}<span>)(\w+)(</span>)',pagefull)
if match_shipping:
  print match_shipping.group(2)



#<h1 itemprop="name">Apple MacBook Pro 13 inch (MD101HN/A)</h1>
#<strong class="redText">Rs <span id="selling-price-id">79999</span></strong>
#<div class="product-free-ship-outer">
#                                                <strong>Shipping Charges</strong>:
#                                                        <span>Free</span>
#                                            </div>
#<strong>5 business days </strong>
#<span><strong>Dispatched</strong> in <strong>3 business days </strong></span>
