import scraperwiki

import re
import urllib2

url = "http://www.flipkart.com/lenovo-essential-g580-59-324061-laptop-3rd-gen-ci5-4gb-500gb-dos/p/itmdcjhugdtpfzrr?pid=COMDAYTZUZWSVDPQ&ref=07a82908-cf28-45ac-99bf-fab8aba546a0"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1.{0,100}">)([\w\s\d\(\)\-\/]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'<div.fk-font-finalprice fk-font-big fk-bold final-price{0,50}">',str(line))
  if match_price:
    print match_price.group()



#<h1 itemprop="name" title="Lenovo Essential G580 (59-324061) Laptop (3rd Gen Ci5/ 4GB/ 500GB/ DOS)">Lenovo Essential G580 (59-324061) Laptop (3rd Gen Ci5/ 4GB/ 500GB/ DOS)</h1>

#<div class="stock-status instock fk-font-normal fk-bold" id="fk-stock-info-id">Available.</div>

#<span class="fk-font-finalprice fk-font-big fk-bold final-price"> Rs. 34500</span>

