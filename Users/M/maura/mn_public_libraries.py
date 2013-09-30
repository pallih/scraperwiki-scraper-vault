import scraperwiki
html = scraperwiki.scrape('http://www.publiclibraries.com/minnesota.htm')
print html

import lxml.html
root = lxml.html.fromstring(html)

tds = root.cssselect('td.city')
for td in tds:
    print td.text


import scraperwiki
html = scraperwiki.scrape('http://www.publiclibraries.com/minnesota.htm')
print html

import lxml.html
root = lxml.html.fromstring(html)

tds = root.cssselect('td.city')
for td in tds:
    print td.text


