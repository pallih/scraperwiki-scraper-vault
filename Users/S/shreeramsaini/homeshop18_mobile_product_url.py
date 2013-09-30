import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('homeshop18_mobile_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.homeshop18.com.*mobiles-accessories/mobiles/product:\d+/cid:\d+',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1
                   
#http://www.homeshop18.com/micromax-3g-android-full-touch-phone-a100/mobiles-accessories/mobiles/product:30130586/cid:3027/?pos=577

#http://www.homeshop18.com/dell-android-3g-full-touch-phone-venue-thunder/mobiles-accessories/mobiles/product:29058499/cid:3027/?pos=582
import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('homeshop18_mobile_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.homeshop18.com.*mobiles-accessories/mobiles/product:\d+/cid:\d+',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1
                   
#http://www.homeshop18.com/micromax-3g-android-full-touch-phone-a100/mobiles-accessories/mobiles/product:30130586/cid:3027/?pos=577

#http://www.homeshop18.com/dell-android-3g-full-touch-phone-venue-thunder/mobiles-accessories/mobiles/product:29058499/cid:3027/?pos=582
