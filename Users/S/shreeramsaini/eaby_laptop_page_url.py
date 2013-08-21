import scraperwiki

import re
import urllib2

url = "http://www.ebay.in/sch/Laptops-/16159/i.html?LH_BIN=1&LH_ItemCondition=1&_trkparms=65%253A12%257C66%253A1%257C39%253A6%257C72%253A3276&rt=nc&_dmd=2&_dmpt=IN_PC_Laptops&_trksid=p3286.c0.m14.l1513&_pgn=1"
openpage = urllib2.urlopen(url)
lines = openpage.readlines()
print type(lines)

count=37
i=0
while i<count:
 path = "%s%d" % ('http://www.ebay.in/sch/Laptops-/16159/i.html?LH_BIN=1&LH_ItemCondition=1&_trkparms=5%253A12%257C66%253A1%257C39%253A6%257C72%253A3276&rt=nc&_dmd=2&_dmpt=IN_PC_Laptops&_trksid=p3286.c0.m14.l1513&_pgn=',i)
 print path
 scraperwiki.sqlite.save(['url'],data={'url':path})
 i=i+1