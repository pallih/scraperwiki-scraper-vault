import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.bleedingcool.com/2013/01/14/top-100-comics/")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='entry-content'] tr"):
    tds = tr.cssselect("td")
    if len(tds)=200:
        data = {
            'QTY_RANK' : tds[0].text_content(),
            'DESCRIPTION' : int(tds[3].text_content())
        }
        print data
