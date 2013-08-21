import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'year' : tds[1].text_content(),
      'men' : tds[7].text_content(),
      'women' : tds[9].text_content(),
      'total' : int(tds[4].text_content())
    }
 #   print data

    scraperwiki.sqlite.save(unique_keys=['country','year','men','women','total'], data=data)
