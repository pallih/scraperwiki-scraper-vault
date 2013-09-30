import scraperwiki

import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://live.nrlstats.com/nrl/season2012.html")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
        'country' : tds[0].text_content(),
        'years_in_school' : int(tds[4].text_content())
 }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)

import scraperwiki

import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://live.nrlstats.com/nrl/season2012.html")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
        'country' : tds[0].text_content(),
        'years_in_school' : int(tds[4].text_content())
 }
    scraperwiki.sqlite.save(unique_keys=['date'], data=data)

