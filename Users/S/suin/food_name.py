import scraperwiki

import scraperwiki

html = scraperwiki.scrape("http://ndb.nal.usda.gov/ndb/search/list")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='list-left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'num' : tds[0].text_content(),
            'description' : tds[1].text_content(),
            'group' : tds[2].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['num'], data=data)

