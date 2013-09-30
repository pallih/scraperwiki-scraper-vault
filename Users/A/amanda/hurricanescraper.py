import scraperwiki

import scraperwiki           

html = scraperwiki.scrape("http://weather.unisys.com/hurricane/atlantic/index.html")

import lxml.html           
root = lxml.html.fromstring(html)
print root.cssselect("a img").length
for tr in root.cssselect("a img"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)


scraperwiki.scrape(url[, params][,user_agent])

import scraperwiki

import scraperwiki           

html = scraperwiki.scrape("http://weather.unisys.com/hurricane/atlantic/index.html")

import lxml.html           
root = lxml.html.fromstring(html)
print root.cssselect("a img").length
for tr in root.cssselect("a img"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)


scraperwiki.scrape(url[, params][,user_agent])

