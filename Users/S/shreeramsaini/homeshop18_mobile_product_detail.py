import scraperwiki

import re
import urllib2

scraperwiki.sqlite.attach('homeshop18_mobile_product_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

count = 0
shipping = "paid"
stock = "out"

for url in urls:
 listurl = url.values()
 productlink = listurl[0]  
 open = urllib2.urlopen(productlink)
 product = open.readlines() 
 pagefull = str(product)

 for line in product:
   match_title = re.search(r'(<h1 id="productLayoutForm:pbiName">)([\w\s\d\(\)\']+)',str(line))
   if match_title:
     title = match_title.group(2)

   match_price = re.search(r'(itemprop="price".*Rs.)([\s\w\d\.]+)',str(line))
   if match_price:
     price = match_price.group(2)

   match_delivery_time = re.search(r'(.*Delivered in)([\s\w\d\-]+)',str(line))
   if match_delivery_time:
     delivery = match_delivery_time.group(2)


 match_shp = re.search(r'(<em>)([\w]+)',pagefull)
 if match_shp:
     shipping = "Free"         

 match_stock = re.search(r'(Availability.*content="in_stock">)([\w]+)',pagefull)
 if match_stock:
     stock = match_stock.group(2)

 count = count + 1
 scraperwiki.sqlite.save(['url'],data={'id':count,'imgpath':title,'url':url,'title':title,'price':price,'shipping':shipping,'delivery':delivery,'stock':stock,'graphics':'','os':'','hd':'','ram':'','subtitle':'','brand':'','display':'','frequency':'','seller_type':'','seller_name':'homeshop18','no_sellers':'1','status':'0','insert_status':'0'})    
import scraperwiki

import re
import urllib2

scraperwiki.sqlite.attach('homeshop18_mobile_product_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

count = 0
shipping = "paid"
stock = "out"

for url in urls:
 listurl = url.values()
 productlink = listurl[0]  
 open = urllib2.urlopen(productlink)
 product = open.readlines() 
 pagefull = str(product)

 for line in product:
   match_title = re.search(r'(<h1 id="productLayoutForm:pbiName">)([\w\s\d\(\)\']+)',str(line))
   if match_title:
     title = match_title.group(2)

   match_price = re.search(r'(itemprop="price".*Rs.)([\s\w\d\.]+)',str(line))
   if match_price:
     price = match_price.group(2)

   match_delivery_time = re.search(r'(.*Delivered in)([\s\w\d\-]+)',str(line))
   if match_delivery_time:
     delivery = match_delivery_time.group(2)


 match_shp = re.search(r'(<em>)([\w]+)',pagefull)
 if match_shp:
     shipping = "Free"         

 match_stock = re.search(r'(Availability.*content="in_stock">)([\w]+)',pagefull)
 if match_stock:
     stock = match_stock.group(2)

 count = count + 1
 scraperwiki.sqlite.save(['url'],data={'id':count,'imgpath':title,'url':url,'title':title,'price':price,'shipping':shipping,'delivery':delivery,'stock':stock,'graphics':'','os':'','hd':'','ram':'','subtitle':'','brand':'','display':'','frequency':'','seller_type':'','seller_name':'homeshop18','no_sellers':'1','status':'0','insert_status':'0'})    
