import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://fczb.de/fortbildung.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")

    tds = [td.text_content().encode('utf-8').replace("&quot;", "") for td in tds]

    if len(tds)>1:
        data = {'Titel' : tds[0],'Datum' : tds[1], 'Untertitel' : tds[2]}

        print data
        scraperwiki.sqlite.save(['Titel','Datum'], data)

