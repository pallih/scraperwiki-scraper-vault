import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/digital-cameras/categoryid:3178/search:*/start:0/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<span.*Digital Cameras.{0,20}',str(line))
  if match_item:  
   print match_item.group()


count=120
i=0
while i<count:
 path= "%s%d" % ('http://www.homeshop18.com/digital-cameras/categoryid:3178/search:*/start:',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+24

#<div class="browse_result_title"><span class="orange_highlight">Digital Cameras</span> (120) </div>
import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/digital-cameras/categoryid:3178/search:*/start:0/"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<span.*Digital Cameras.{0,20}',str(line))
  if match_item:  
   print match_item.group()


count=120
i=0
while i<count:
 path= "%s%d" % ('http://www.homeshop18.com/digital-cameras/categoryid:3178/search:*/start:',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+24

#<div class="browse_result_title"><span class="orange_highlight">Digital Cameras</span> (120) </div>
