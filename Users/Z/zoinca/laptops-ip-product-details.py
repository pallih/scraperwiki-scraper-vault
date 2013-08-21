import scraperwiki

# Blank Python
import urllib2
import re

scraperwiki.sqlite.attach('laptops-ip-products-urls','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

for dict_urls in list_urls:
 url = dict_urls['url']
 open = urllib2.urlopen(url)
 page = str(open.readlines())
 openlines = urllib2.urlopen(url)
 lines = openlines.readlines()
 
 print url
 
 match_title = re.search(r'(<span itemprop="name">[\S\w]+)(\W+)([+.,\'\(\)\"\w\d\s&-/]+)',page)
 #match_title = re.search(r',page)
 if match_title:
  print 'title : '+match_title.group(3)
  title = match_title.group(3)

 match_price = re.search(r'(<span class="blueFont">.{0,3}Rs.\s+)(\d+)',page)
 if match_price:
  #print match_price.group()
  price = match_price.group(2)
  print 'price : '+price

 match_delivery = re.search(r'(delDateQuest.{0,3}>[\w\s]+)(\d+)',page)
 if match_delivery:
  #print match_price.group()
  delivery = match_delivery.group(2)
  print 'delivery : '+delivery
 
 for line in lines:
  #print line
  match_image = re.search(r'class.{0,4}jqzoom.*id.{0,4}demo1',line)
  if match_image:
   print line
   match_image_url = re.search(r'(http://images.indiaplaza.com/)([-/\w\d]+..{3,4})',line)
   if match_image_url:
    image_url = match_image_url.group()
    image_path = match_image_url.group(2)
    print "image_path : "+image_path
 scraperwiki.sqlite.save(['url'],data={'url':url,'title':title,'price':price,'delivery':delivery,'shipping':'Free','stock':'In','image_url':image_url,'image_path':image_path})

#<a title="" href="http://images.indiaplaza.com/pcstore/images/PC17032012FUJITSU01-L.jpg" class="jqzoom" id="demo1" rel="gal1" style="margin-bottom: 10px; outline-style: none; text-decoration: none;"><div class="zoomPad"><img style="opacity: 1;" src="http://images.indiaplaza.com/pcstore/images/PC17032012FUJITSU01-L.jpg" alt="fujitsu amilo si3655 notebook" title="fujitsu amilo si3655 notebook" id="my_image" height="260px" width="260px"><div style="display: none; top: -1px; left: -1px; width: 260px; height: 260px; position: absolute; border-width: 1px;" class="zoomPup"></div><div style="position: absolute; z-index: 5001; left: 270px; top: 0px; display: none;" class="zoomWindow"><div style="width: 350px; margin-top: -50px;" class="zoomWrapper"><div style="width: 100%; position: absolute; display: none;" class="zoomWrapperTitle"></div><div style="width: 100%; height: 350px;" class="zoomWrapperImage"><img src="http://images.indiaplaza.com/pcstore/images/PC17032012FUJITSU01-L.jpg" style="position: absolute; border: 0px none; display: block; left: 0px; top: 0px;"></div></div></div><div style="visibility: hidden; top: 105.5px; left: 80px; position: absolute;" class="zoomPreload">Loading zoom</div></div></a>

