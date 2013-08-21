import scraperwiki
import lxml.html

root = lxml.html.fromstring(html)
tds = root.cssselect('td')
for td in tds:
    print lxml.html.tostring(td)
    print td.text