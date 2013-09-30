import scraperwiki

# Blank Python

import urllib2
import re
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

url = 'http://www.snapdeal.com/products/computers-laptops?sort=plrty&storeID=computers-laptops_viewall'

open = urllib2.urlopen(url)
page = str(open.readlines())
matches = re.findall(r'hit-ss-logger.{5,500}title',page)
count=0
for match in matches:
 print match
 count = count+1
 print count

 #http = httplib2.Http()
 #status, response = http.request(url)

 links = []

 for link in BeautifulSoup(str(match), parseOnlyThese=SoupStrainer('a')):
  if link.has_key('href'):
   #print 'inside if of href'
   url = link['href']
   print url


#[/\w?&;=-]+pid=[\d\w]+
#<a class="hit-ss-logger" v="p" categoryid="21" href="http://www.snapdeal.com/product/SamsungNP9/60313?pos=245;248" title="Samsung NP900X1B-A01IN Netbook (Black)" pogid="60313"><div class="product-image"><img src="http://i1.sdlcdn.com/img/product/main/166x194/Samsung_NP900X1B_A01IN_Netbook_Black_M_1_2xA.jpg" alt="Samsung NP900X1B-A01IN Netbook (Black)" border="0" height="194" width="166"></div><div class="product_listing_heading">Samsung NP900X1B-A01IN Netbook (Black)</div><div class="product_listing_price_outer"><div class="product_price "><span class="originalprice ">Rs&nbsp;86990</span>  Rs&nbsp;74699</div><div class="product_discount_outer"><div class="product_discount">14% <span>Off</span></div></div></div></a>
import scraperwiki

# Blank Python

import urllib2
import re
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

url = 'http://www.snapdeal.com/products/computers-laptops?sort=plrty&storeID=computers-laptops_viewall'

open = urllib2.urlopen(url)
page = str(open.readlines())
matches = re.findall(r'hit-ss-logger.{5,500}title',page)
count=0
for match in matches:
 print match
 count = count+1
 print count

 #http = httplib2.Http()
 #status, response = http.request(url)

 links = []

 for link in BeautifulSoup(str(match), parseOnlyThese=SoupStrainer('a')):
  if link.has_key('href'):
   #print 'inside if of href'
   url = link['href']
   print url


#[/\w?&;=-]+pid=[\d\w]+
#<a class="hit-ss-logger" v="p" categoryid="21" href="http://www.snapdeal.com/product/SamsungNP9/60313?pos=245;248" title="Samsung NP900X1B-A01IN Netbook (Black)" pogid="60313"><div class="product-image"><img src="http://i1.sdlcdn.com/img/product/main/166x194/Samsung_NP900X1B_A01IN_Netbook_Black_M_1_2xA.jpg" alt="Samsung NP900X1B-A01IN Netbook (Black)" border="0" height="194" width="166"></div><div class="product_listing_heading">Samsung NP900X1B-A01IN Netbook (Black)</div><div class="product_listing_price_outer"><div class="product_price "><span class="originalprice ">Rs&nbsp;86990</span>  Rs&nbsp;74699</div><div class="product_discount_outer"><div class="product_discount">14% <span>Off</span></div></div></div></a>
