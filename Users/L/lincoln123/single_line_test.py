import scraperwiki
html = scraperwiki.scrape("http://xiaoyongzi.github.io/web/newsroom.html")

import lxml.html           
root = lxml.html.fromstring(html)
aa = root.cssselect("a[href='newsroom_2.html']").pop()
bb = aa.text
print repr(bb)
print bb

