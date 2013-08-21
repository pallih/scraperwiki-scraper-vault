import scraperwiki

# Blank Python
html = scraperwiki.scrape("http://espn.go.com/nba/standings")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr[align=right]"):
    tds = tr.cssselect("td")
    data = {
      'Name' : tds[0].text_content(),
      'W' : tds[1].text_content(),
      'L' : tds[2].text_content(),
      'PCT' : tds[3].text_content(),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['Name', 'W', 'L', 'PCT'], data=data)
