import scraperwiki
html = scraperwiki.scrape("http://singaporeseen.stomp.com.sg/singaporeseen/")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("<div class>"):
    tds = tr.cssselect("td")
    print len(tds)
       

