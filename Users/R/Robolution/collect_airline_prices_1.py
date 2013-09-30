import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.inner a"): print el

scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Hi there"})

# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.kayak.com/#flights/CLE-SIN/2012-05-30/2012-08-30")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.inner a"): print el

scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Hi there"})

# Blank Python

