import scraperwiki

import re
import urllib2

url = "http://www.naaptol.com/tablet/mtnl-teracom-lofty-tz300-tablet/P/12149271.html"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1>)([\w\s\d]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'<span class="rsSymbol">.{0,50}[\w\d\,]+',str(line))   #multi record found
  if match_price:
    print match_price.group()
  match_shp = re.search(r'(<span class="rsSymbol">)([\w\d\s\.]+)',str(line))
  if match_shp:
    print match_shp.group()

#<h1>MTNL Teracom Lofty TZ300 tablet</h1>

#<strong><span class="rsSymbol">`</span> 3,299</strong>

#<span style="color:black;font-size:11px;font-weight:normal;"><b>Shipping Charges: </b> <span class="rsSymbol">`</span> 99 only.</span>
import scraperwiki

import re
import urllib2

url = "http://www.naaptol.com/tablet/mtnl-teracom-lofty-tz300-tablet/P/12149271.html"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
pagefull = str(lines)
print type(lines)

for line in lines:
  match_title = re.search(r'(<h1>)([\w\s\d]+)',str(line))
  if match_title:
    print match_title.group(2)
  match_price = re.search(r'<span class="rsSymbol">.{0,50}[\w\d\,]+',str(line))   #multi record found
  if match_price:
    print match_price.group()
  match_shp = re.search(r'(<span class="rsSymbol">)([\w\d\s\.]+)',str(line))
  if match_shp:
    print match_shp.group()

#<h1>MTNL Teracom Lofty TZ300 tablet</h1>

#<strong><span class="rsSymbol">`</span> 3,299</strong>

#<span style="color:black;font-size:11px;font-weight:normal;"><b>Shipping Charges: </b> <span class="rsSymbol">`</span> 99 only.</span>
