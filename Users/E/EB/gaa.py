import scraperwiki
html = scraperwiki.scrape("http://gaa.ie/clubzone/club-info/find-a-club/")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'county' : tds[0].text_content(),
      'club' : int(tds[4].text_content())
    }
scraperwiki.sqlite.save(unique_keys=['county'], data=data)

import scraperwiki
html = scraperwiki.scrape("http://gaa.ie/clubzone/club-info/find-a-club/")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'county' : tds[0].text_content(),
      'club' : int(tds[4].text_content())
    }
scraperwiki.sqlite.save(unique_keys=['county'], data=data)

