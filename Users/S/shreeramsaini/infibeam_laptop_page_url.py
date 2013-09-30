import scraperwiki

import re
import urllib2

url = "http://www.infibeam.com/Laptop_Computers_Accessories/#category=Laptop&store=Computers_Accessories&page=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'Showing*<b>\d+',str(line))
  if match_item:  
   print match_item.group()


count=11
i=1
while i<=count:
 path= "%s%d" % ('http://www.infibeam.com/Laptop_Computers_Accessories/#category=Laptop&store=Computers_Accessories&page=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1

#<div style="line-height:24px;">Showing <b>1-20</b> of <b>210</b>  </div>
import scraperwiki

import re
import urllib2

url = "http://www.infibeam.com/Laptop_Computers_Accessories/#category=Laptop&store=Computers_Accessories&page=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'Showing*<b>\d+',str(line))
  if match_item:  
   print match_item.group()


count=11
i=1
while i<=count:
 path= "%s%d" % ('http://www.infibeam.com/Laptop_Computers_Accessories/#category=Laptop&store=Computers_Accessories&page=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1

#<div style="line-height:24px;">Showing <b>1-20</b> of <b>210</b>  </div>
