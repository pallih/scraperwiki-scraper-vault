import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.montrealjazzfest.com/program/Default.aspx')
root = lxml.html.fromstring(html)
trs = root.cssselect("table.grilleConcertsJours tr")

for tr in trs:
    print lxml.html.tostring(tr)

import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.montrealjazzfest.com/program/Default.aspx')
root = lxml.html.fromstring(html)
trs = root.cssselect("table.grilleConcertsJours tr")

for tr in trs:
    print lxml.html.tostring(tr)

