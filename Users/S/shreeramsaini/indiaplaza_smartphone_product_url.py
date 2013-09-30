import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('indiaplaza_smartphone_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.indiaplaza.com.*phones-mobiles.{0,50}',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1

#http://www.indiaplaza.com/intel-xolo-x-500-smart-phones-mobiles-mob29012013int001-10.htm

#http://www.indiaplaza.com/apple-iphone-5-smart-phones-mobiles-mob17092012app01-10.htm

import scraperwiki

import urllib2
import re

scraperwiki.sqlite.attach('indiaplaza_smartphone_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'http://www.indiaplaza.com.*phones-mobiles.{0,50}',str(line))
  if match_product_url:
    purl = match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print count
    count = count + 1

#http://www.indiaplaza.com/intel-xolo-x-500-smart-phones-mobiles-mob29012013int001-10.htm

#http://www.indiaplaza.com/apple-iphone-5-smart-phones-mobiles-mob17092012app01-10.htm

