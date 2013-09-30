import scraperwiki
html = scraperwiki.scrape('http://www.takoa.co.nz/iwi_scholar1.htm')

import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('p')
for p in tds:
    print lxml.html.tostring(p)
    print p.text


import scraperwiki
html = scraperwiki.scrape('http://www.takoa.co.nz/iwi_scholar1.htm')

import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('p')
for p in tds:
    print lxml.html.tostring(p)
    print p.text


