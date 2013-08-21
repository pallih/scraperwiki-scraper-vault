import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/laptops/categoryid:3291/search:*/sort:Best+Sellers/start:0/inStock:true/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'(<span class="orange_highlight)(.{0,50})',str(line))
  if match_item:  
   print match_item.group(2)


count=269
i=0
while i<count:
 path= "%s%d%s" % ('http://www.homeshop18.com/laptops/categoryid:3291/search:*/sort:Best+Sellers/start:',i,'/inStock:true/')
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+24

