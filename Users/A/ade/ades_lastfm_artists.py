import lxml.html           
import scraperwiki

html = scraperwiki.scrape("http://www.last.fm/user/netclectic/charts?rangetype=overall&subtype=artists")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='candyStriped chart'] tbody tr"):
    tds = tr.cssselect("td")
    data = {
      'artist' : tds[2].text_content().replace("\n", "").strip(" "),
      'scrobbles' : int(tds[5].text_content().replace(",", "").strip("\n").strip(" "))
    }
    scraperwiki.sqlite.save(unique_keys=['artist'], data=data)