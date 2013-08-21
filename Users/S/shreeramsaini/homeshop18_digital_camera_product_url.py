import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('homeshop18_digital_camera_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')


for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.homeshop18.com.*camera-camcorders/digital-cameras/product:\d+/cid:\d+',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1

