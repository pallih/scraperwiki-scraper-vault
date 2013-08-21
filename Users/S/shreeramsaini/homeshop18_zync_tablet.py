import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/zync-z99-7-2g-calling/computer-peripherals/ipads-tablets/product:30409402/cid:8937/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1 id="productLayoutForm:pbiName">)([\w\s\d\(\)\']+)',str(line))
  if match_title:
    print match_title.group(2)

  match_price = re.search(r'(itemprop="price".*Rs.)([\s\w\d\.]+)',str(line)) 
  if match_price:
    print match_price.group(2)

  match_delivery_time = re.search(r'(.*Delivered in)([\s\w\d\-]+)',str(line))
  if match_delivery_time:
    print match_delivery_time.group(2)


match_shp = re.search(r'(<em>)([\w]+)',pagefull)
if match_shp:
    print match_shp.group(2)

match_stock = re.search(r'(Availability.*content="in_stock">)([\w]+)',pagefull)
if match_stock:
    print match_stock.group(2)

