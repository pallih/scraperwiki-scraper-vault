import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.nav"):
    print el

import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.nav"):
    print el

