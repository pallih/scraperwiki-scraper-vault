# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://beeradvocate.com/user/beers?ba=Summer78&view=W")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    #if len(tds)==12:
    data = {
        'beer' : tds[1].text_content(),
        'years_in_school' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://beeradvocate.com/user/beers?ba=Summer78&view=W")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    #if len(tds)==12:
    data = {
        'beer' : tds[1].text_content(),
        'years_in_school' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
