import scraperwiki
html = scraperwiki.scrape("http://www.sardegnasociale.it/index.php?xsl=348&s=11&v=9&c=3371&c1=2123&pv=1&nc=1")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

import scraperwiki
html = scraperwiki.scrape("http://www.sardegnasociale.it/index.php?xsl=348&s=11&v=9&c=3371&c1=2123&pv=1&nc=1")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

