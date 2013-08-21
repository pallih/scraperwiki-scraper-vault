import scraperwiki
import urlparse
import lxml.html
import StringIO
from lxml import etree

html = scraperwiki.scrape("http://qpublic4.qpublic.net/ga_display.php?county=ga_dawson&KEY=105%20%20%20%20019&")
print html
tree = etree.parse(html)
r= tree.findtext("//*")
print r
#r = tree.xpath('/html//table[2]//tr[6]//td[2]')
#r = tree.xpath('/html')
#print r
#len(r)
#print len(r)
#print r[0].tag
