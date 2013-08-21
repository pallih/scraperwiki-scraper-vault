import scraperwiki
html = scraperwiki.scrape("http://www.infoplease.com/ipea/A0004420.html")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='sgmltable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'rank' : tds[0].text_content(),
            'newspaper' : tds[1].text_content(),
            'circulation' : tds[2].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['rank'], data=data)
