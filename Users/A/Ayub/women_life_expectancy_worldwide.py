# Example Scrapper

import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/health.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'Women Life Expectancy Worldwide ' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

