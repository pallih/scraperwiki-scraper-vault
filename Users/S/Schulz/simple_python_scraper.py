import scraperwiki 
import lxml.html

html = scraperwiki.scrape("http://www.hnd.bayern.de/tabellen/tabelle_pegel.php?zp=1")

root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==9:
        data = {
            "Ort":tds[0].text_content(),
            "Wasser":tds[1].text_content(),
            "Pegel":tds[3].text_content()
        }
        data = data.strip()
        scraperwiki.sqlite.save(unique_keys=['Ort'], data=data)
import scraperwiki 
import lxml.html

html = scraperwiki.scrape("http://www.hnd.bayern.de/tabellen/tabelle_pegel.php?zp=1")

root = lxml.html.fromstring(html)
for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==9:
        data = {
            "Ort":tds[0].text_content(),
            "Wasser":tds[1].text_content(),
            "Pegel":tds[3].text_content()
        }
        data = data.strip()
        scraperwiki.sqlite.save(unique_keys=['Ort'], data=data)
