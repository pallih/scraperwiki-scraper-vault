import scraperwiki

import re
import urllib2

url = "http://www.snapdeal.com/product/acer-gateway-ne56r-laptop-2nd/430592?storeID=computers-laptops_wdgt4in1_430592"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1 itemprop="name">)([\s\w\(\)/]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'(selling.{0,50}">)(\d+)',str(line))
  if match_price:
    print match_price.group(2)
  match_desp = re.search(r'(Dispatched.{0,50})(\d+[\s\w]+)',str(line))
  if match_desp:
    print match_desp.group(2)

match_spc = re.search(r'(Shipping Charge.{0,100})(<span>.{0,50})(</span>)',pagefull)
if match_spc:
  print match_spc.group(2)



#<h1 itemprop="name">Acer Gateway NE56R Laptop (2nd Gen PDC/ 2GB/ 500GB/ Linux/ 128MB Graph)</h1> - (<h1 itemprop="name">)(.{0,500})(</h1>)
#<strong class="redText">Rs <span id="selling-price-id">20700</span></strong>
#<li class="shippingSpace"><span><strong>Dispatched</strong> in <strong>3 business days </strong></span></li>
#<div class="product-free-ship-outer">
#                                                <strong>Shipping Charges</strong>:
#                                                       <span>Free</span>
#                                           </div>

