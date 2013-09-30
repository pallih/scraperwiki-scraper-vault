import scraperwiki
html = scraperwiki.scrape("http://www.fortmason.org/events?m=12&y=2012&category=all_categories&when=today")
print html

import lxml.html
root = lxml.html.fromstring(html)
for h2 in root.cssselect("h2"):
    data = {'event' : h2.text_content()}
    scraperwiki.sqlite.save(unique_keys=['event'], data=data)

import scraperwiki
html = scraperwiki.scrape("http://www.fortmason.org/events?m=12&y=2012&category=all_categories&when=today")
print html

import lxml.html
root = lxml.html.fromstring(html)
for h2 in root.cssselect("h2"):
    data = {'event' : h2.text_content()}
    scraperwiki.sqlite.save(unique_keys=['event'], data=data)

