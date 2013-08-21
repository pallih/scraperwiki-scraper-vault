import scraperwiki

# Blank Python

import re
import urllib2

scraperwiki.sqlite.attach('laptops-flipkart-producturls','purls')
purls = scraperwiki.sqlite.select('* from purls.swdata')

print purls

count = 0

for purl in purls:
 price = 0 
 url = purl['url']
 print url

 ProductPage = urllib2.urlopen(url)
 lines = ProductPage.readlines()
 
 for line in lines:
   match_title = re.search(r'<h1.*title="(.*)"',str(line))
   if match_title:
    title = match_title.group(1)

   match_price = re.search(r'final-price.{0,100}Rs[\.\s]+([\d]+)',str(line))
   if match_price:
    price = match_price.group(1)
#<span class=" fk-font-big fk-bold final-price"> Rs. 35903</span>


   match_stock = re.search(r'fk-stock-info-id.{0,5}>(\w+)',str(line))
   if match_stock:
    stock = match_stock.group(1)

   match_delivery = re.search(r'([\d\s]+-[\d]+)\s+business\s+days',str(line))
   if match_delivery:
    delivery = match_delivery.group(1)

   match_shipping = re.search(r'FREE\s+Home\s+Delivery',str(line))
   if match_shipping:
    shipping = "Free"
   else:
    shipping = "Paid"
 count = count + 1

 scraperwiki.sqlite.save(['url'],data={'id':count,'imgpath':title,'url':url,'title':title,'price':price,'shipping':shipping,'delivery':delivery,'stock':stock,'graphics':'','os':'','hd':'','ram':'','subtitle':'','brand':'','display':'','frequency':'','seller_type':'','seller_name':'Flipkart','no_sellers':'1','status':'0','insert_status':'0'})    