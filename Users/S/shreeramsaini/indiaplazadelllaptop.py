import scraperwiki

import re
import urllib2

url="http://www.indiaplaza.com/dell-15r-n5520-laptops-pc-pcs20121211del001-10.htm"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)

print type(lines)

for line in lines:
  match_title = re.search(r'(<span.{0,50}lblTitle.{0,10}">)([\w\s\d]+)',str(line))
  if match_title:
    print match_title.group(2)

  match_price = re.search(r'<span id="lblOurPrice" class="price_fdp">[\d\.]+',str(line))
  if match_price:
    print match_price.group()

  match_shp = re.search(r'Free.{0,50}',str(line))    
  if match_shp:
   print match_shp.group()


#<span id="lblShipment">FREE Shipping In 5 Business Days</span>

#<span id="lblOurPrice" class="price_fdp">40889</span>   

