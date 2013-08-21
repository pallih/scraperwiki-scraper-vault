import scraperwiki

import re
import urllib2

scraperwiki.sqlite.attach('infibeam_laptop_page_url',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')

for url in urls:
 listurl = url.values()
 pagelink = listurl[0]  
 open = urllib2.urlopen(pagelink)
 page = open.readlines()
 fullpage=str(page)

 print type(page)

 count = 1
 for line in page: 
  match_product_url = re.search(r'(href=")(/Laptop/[\w\d\-\/\.]+)',fullpage)
  if match_product_url:
    purl = 'www.infibeam.com' + match_product_url.group(2)    
    scraperwiki.sqlite.save(['url'],data={'url':purl})
    print purl
    print count
    count = count + 1

#<a href="/Laptop/i-Samsung-Laptop-NP550P5C-S01IN/P-CA-L-Samsung-NP550P5C-S01IN.html?id=Silver