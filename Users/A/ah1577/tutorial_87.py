import scraperwiki
html = scraperwiki.scrape("http://www.baseball-reference.com/leagues/")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='sgmltable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'Year' : tds[0].text_content(),
            'Lg' : tds[1].text_content(),
            'Champion' : tds[2].text_content()      
        }
        scraperwiki.sqlite.save(unique_keys=['baseball'], data=data)
import scraperwiki
html = scraperwiki.scrape("http://www.baseball-reference.com/leagues/")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='sgmltable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'Year' : tds[0].text_content(),
            'Lg' : tds[1].text_content(),
            'Champion' : tds[2].text_content()      
        }
        scraperwiki.sqlite.save(unique_keys=['baseball'], data=data)
