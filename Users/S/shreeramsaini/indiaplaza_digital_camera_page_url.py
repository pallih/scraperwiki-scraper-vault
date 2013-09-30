import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/digital-cameras-cameras-1.htm?sort=dp&PageNo=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<style.*Digital Cameras.{0,20}',str(line))
  if match_item:  
   print match_item.group()


count=4
i=1
while i<=count:
 path= "%s%d" % ('http://www.indiaplaza.com/digital-cameras-cameras-1.htm?sort=dp&PageNo=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1


#<h1 style="float: left;font-size:15px;color: #292A2A;font-weight: bold;margin-top:-2px;">Digital Cameras</h1><span class="filteresult">(Showing 61 - 65 of 65 products)<span>import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/digital-cameras-cameras-1.htm?sort=dp&PageNo=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<style.*Digital Cameras.{0,20}',str(line))
  if match_item:  
   print match_item.group()


count=4
i=1
while i<=count:
 path= "%s%d" % ('http://www.indiaplaza.com/digital-cameras-cameras-1.htm?sort=dp&PageNo=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1


#<h1 style="float: left;font-size:15px;color: #292A2A;font-weight: bold;margin-top:-2px;">Digital Cameras</h1><span class="filteresult">(Showing 61 - 65 of 65 products)<span>