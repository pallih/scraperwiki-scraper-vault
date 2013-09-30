import scraperwiki

import re
import urllib2

url = "http://www.ebay.in/itm/New-SAMSUNG-NOTE-800-N8000-10-1-TAB-TABLET-Android4-0-GSM-Sim-Slot-16GB-3G-WiFi-/190788181373?pt=IN_iPads_Tablets&hash=item2c6bdc9d7d"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1 class="vi-is1-titleH1">)([\w\s\d\-\.\"\,]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'(<span class="vi-is1-prcp" id="v4-27">)([\w\.\d\,\s]+)',str(line))
  if match_price:
    print match_price.group(2)
  match_shp = re.search(r'(<span class="vi-is1-tese">)([\w]+)',str(line))
  if match_shp:
    print match_shp.group(2)
  match_stock = re.search(r'(<span class="vi-is1-mqtyDiv">)([\d\w\s]+)',str(line))
  if match_stock:
    print match_stock.group(2)



#<h1 class="vi-is1-titleH1">New SAMSUNG NOTE 800 N8000 10.1" TAB TABLET Android4.0 GSM Sim Slot 16GB 3G,WiFi</h1>
#<span class="vi-is1-prcp" id="v4-27">Rs. 43,990.00</span>
#<span class="vi-is1-tese">FREE</span>
#<span class="vi-is1-mqtyDiv">5 available</span>

import scraperwiki

import re
import urllib2

url = "http://www.ebay.in/itm/New-SAMSUNG-NOTE-800-N8000-10-1-TAB-TABLET-Android4-0-GSM-Sim-Slot-16GB-3G-WiFi-/190788181373?pt=IN_iPads_Tablets&hash=item2c6bdc9d7d"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1 class="vi-is1-titleH1">)([\w\s\d\-\.\"\,]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'(<span class="vi-is1-prcp" id="v4-27">)([\w\.\d\,\s]+)',str(line))
  if match_price:
    print match_price.group(2)
  match_shp = re.search(r'(<span class="vi-is1-tese">)([\w]+)',str(line))
  if match_shp:
    print match_shp.group(2)
  match_stock = re.search(r'(<span class="vi-is1-mqtyDiv">)([\d\w\s]+)',str(line))
  if match_stock:
    print match_stock.group(2)



#<h1 class="vi-is1-titleH1">New SAMSUNG NOTE 800 N8000 10.1" TAB TABLET Android4.0 GSM Sim Slot 16GB 3G,WiFi</h1>
#<span class="vi-is1-prcp" id="v4-27">Rs. 43,990.00</span>
#<span class="vi-is1-tese">FREE</span>
#<span class="vi-is1-mqtyDiv">5 available</span>

