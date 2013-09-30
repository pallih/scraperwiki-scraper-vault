import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/mobiles/categoryid:14569/search:*/start:24"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<span class="orange_highlight">Mobiles.{0,50}',str(line))
  if match_item:  
   print match_item.group()


count=588
i=0
while i<count:
 path = "%s%d" % ('http://www.homeshop18.com/mobiles/categoryid:14569/search:*/start:',+i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+24

#<div class="browse_result_title"><span class="orange_highlight">Mobiles</span> (588) </div>
import scraperwiki

import re
import urllib2

url = "http://www.homeshop18.com/mobiles/categoryid:14569/search:*/start:24"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

for line in lines:
  match_item = re.search(r'<span class="orange_highlight">Mobiles.{0,50}',str(line))
  if match_item:  
   print match_item.group()


count=588
i=0
while i<count:
 path = "%s%d" % ('http://www.homeshop18.com/mobiles/categoryid:14569/search:*/start:',+i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+24

#<div class="browse_result_title"><span class="orange_highlight">Mobiles</span> (588) </div>
