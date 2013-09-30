import scraperwiki
html = scraperwiki.scrape("http://www.infoplease.com/ipea/A0301522.html")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='sgmltable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'rank' : tds[0].text_content(),
            'magazine' : tds[1].text_content(),
            'total paid circulation' : tds[2].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['rank'], data=data)
import scraperwiki
html = scraperwiki.scrape("http://www.infoplease.com/ipea/A0301522.html")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='sgmltable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'rank' : tds[0].text_content(),
            'magazine' : tds[1].text_content(),
            'total paid circulation' : tds[2].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['rank'], data=data)
