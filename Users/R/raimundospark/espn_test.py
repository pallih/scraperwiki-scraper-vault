import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://espn.go.com/mens-college-basketball/team/_/id/38/colorado-buffaloes")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("td[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'points' : tds[0].text_content(),
      'ppg' : int(tds[1].text_content())
    }
    print data
    print tds[1].text_content()

