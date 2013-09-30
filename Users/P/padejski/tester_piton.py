import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.acas.rs/acasPublic/izvestajDetails.htm?parent=pretragaIzvestaja&izvestajId=1")
root = lxml.html.fromstring(html)
for td in root.cssselect("div.funkcionerSearchDiv h4"):
    scraperwiki.sqlite.save(unique_keys=['country'], data=td)import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.acas.rs/acasPublic/izvestajDetails.htm?parent=pretragaIzvestaja&izvestajId=1")
root = lxml.html.fromstring(html)
for td in root.cssselect("div.funkcionerSearchDiv h4"):
    scraperwiki.sqlite.save(unique_keys=['country'], data=td)