import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('eaby_laptop_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.eaby.in/itm.*?pt=IN_PC_Laptops&hash=item\d+',str(page))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1

#http://www.ebay.in/itm/SONY-VAIO-E-Series-Laptop-SVE15111EN-B970-2-30ghz-2-320-15-5-W7HB-/150971194664?pt=IN_PC_Laptops&hash=item2326959d28

#http://www.ebay.in/itm/New-HP-Pavilion-15-b002TX-15-6-3rdGen-Corei3-2GB-500GB-Win8-1GB-Graph-SleekBook-/190794200666?pt=IN_PC_Laptops&hash=item2c6c38765a
import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('eaby_laptop_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.eaby.in/itm.*?pt=IN_PC_Laptops&hash=item\d+',str(page))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1

#http://www.ebay.in/itm/SONY-VAIO-E-Series-Laptop-SVE15111EN-B970-2-30ghz-2-320-15-5-W7HB-/150971194664?pt=IN_PC_Laptops&hash=item2326959d28

#http://www.ebay.in/itm/New-HP-Pavilion-15-b002TX-15-6-3rdGen-Corei3-2GB-500GB-Win8-1GB-Graph-SleekBook-/190794200666?pt=IN_PC_Laptops&hash=item2c6c38765a
