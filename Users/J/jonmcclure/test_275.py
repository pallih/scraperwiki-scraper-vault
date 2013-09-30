import scraperwiki
html = scraperwiki.scrape("http://fantasy.mlssoccer.com/player-list/")
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    print





# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://fantasy.mlssoccer.com/player-list/")
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div tr"):
    tds = tr.cssselect("td")
    print





# Blank Python

