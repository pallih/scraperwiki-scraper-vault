import scraperwiki
html = scraperwiki.scrape("http://statline.cbs.nl/StatWeb/publication/?VW=T&DM=SLNL&PA=37683&HD=111022-1438&HDR=T&STB=G1,G2,G3")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'onderwerpen' : tds[0].text_content(),
      'Totaal niet-natuurlijke dood' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['onderwerpen'], data=data)
