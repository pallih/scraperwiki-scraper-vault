import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/smart-phones-mobiles-1.htm?sort=dp&PageNo=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

count=5
i=1
while i<=count:
 path = "%s%d" % ('http://www.indiaplaza.com/smart-phones-mobiles-1.htm?sort=dp&PageNo=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1

import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/smart-phones-mobiles-1.htm?sort=dp&PageNo=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

count=5
i=1
while i<=count:
 path = "%s%d" % ('http://www.indiaplaza.com/smart-phones-mobiles-1.htm?sort=dp&PageNo=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1

