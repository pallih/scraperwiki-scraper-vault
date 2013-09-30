import scraperwiki

# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20101224065234/http://unstats.un.org/unsd/demographic/products/socind/unemployment.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country_or_area' : tds[0].text_content(),
      'total' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country_or_area'], data=data)

import scraperwiki

# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20101224065234/http://unstats.un.org/unsd/demographic/products/socind/unemployment.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country_or_area' : tds[0].text_content(),
      'total' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country_or_area'], data=data)

