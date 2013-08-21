import scraperwiki

import re
import urllib2

url = "http://www.infibeam.com/Laptop/i-Toshiba-Gaming-Laptop-C850D-M5010/P-CA-L-Toshiba-C850D-M5010.html?id=Black"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<span class="item">)([\w\s\d\-]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'(<span class="infiPrice amount price">)([\d\,]+)',str(line))
  if match_price:
    print match_price.group(2)
  match_shp = re.search(r'<b>.Shipping.{0,50}[\w\s\!]+',str(line)) #not work
  if match_shp:
    print match_shp.group()

match_desp = re.search(r'(Ships in<b>.)([\d\-\w\s]+)',pagefull)
if match_desp:
  print match_desp.group(2)

match_stock = re.search(r'(<span class="status">).([\w\s]+.{0,15})',pagefull)
if match_stock:
  print match_stock.group(2)


#<b> FREE Shipping in India! </b>

#<span class="status">
#In Stock.
#</span>

#<span class="shippingTimeSpan">
#Ships in <b>2-3 business days</b>.
#</span>
