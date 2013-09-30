import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://www.occupytogether.org/actions/")
print html
import lxml.html
root = lxml.html.fromstring(html)
for el in root.cssselect("div.post-entry"):
    print el
    print lxml.html.tostring(el)
el = root.cssselect("tr.cont")
print el

import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://www.occupytogether.org/actions/")
print html
import lxml.html
root = lxml.html.fromstring(html)
for el in root.cssselect("div.post-entry"):
    print el
    print lxml.html.tostring(el)
el = root.cssselect("tr.cont")
print el

