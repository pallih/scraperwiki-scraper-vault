import scraperwiki

scraperwiki.sqlite.attach('indiaplaza_digital_camera_page_url','urls')
urls = scraperwiki.sqlite.select('* from urls.swdata')

import urllib2
import re

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 count = 1
 for line in page:
  match_product_url = re.search(r'.*cameras-cam.\d\d\d\d\d\d\d\d[\w\d\-\.]+',str(line))
  if match_product_url:
    purl = 'http://www.indiaplaza.com/' + match_product_url.group()
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print purl
    print count
    count = count + 1

#http://www.indiaplaza.com/sony-cybershot-dsc-w690-digital-cameras-cameras-cam20120521gir001-10.htm

#http://www.indiaplaza.com/fujifilm-finepix-x10-cameras-cam20111226thr001-10.htm


