import scraperwiki

# Blank Python
import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://livingwage.mit.edu/counties/01001")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'expenses_table' : tds[0].text_content(),
            'living wages' : int(tds[4].text_content())
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki

# Blank Python
import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://livingwage.mit.edu/counties/01001")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'expenses_table' : tds[0].text_content(),
            'living wages' : int(tds[4].text_content())
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
