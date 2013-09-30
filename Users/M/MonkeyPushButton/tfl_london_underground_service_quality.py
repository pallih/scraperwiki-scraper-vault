import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.tfl.gov.uk/")
root = lxml.html.fromstring(html) 

now = datetime.datetime.now()

for el in root.cssselect("table.service-board-tbl tr"): 
    print lxml.html.tostring(el)
    cells = el.cssselect("td")
    if len(cells) == 0:
        continue
    line = cells[0].text
    service_quality = cells[1].cssselect("div")[0].text
    scraperwiki.sqlite.save(unique_keys=["line", "date_saved"], data={"line":line, "date_saved":now, "service_quality":service_quality})import scraperwiki
import lxml.html
import datetime

html = scraperwiki.scrape("http://www.tfl.gov.uk/")
root = lxml.html.fromstring(html) 

now = datetime.datetime.now()

for el in root.cssselect("table.service-board-tbl tr"): 
    print lxml.html.tostring(el)
    cells = el.cssselect("td")
    if len(cells) == 0:
        continue
    line = cells[0].text
    service_quality = cells[1].cssselect("div")[0].text
    scraperwiki.sqlite.save(unique_keys=["line", "date_saved"], data={"line":line, "date_saved":now, "service_quality":service_quality})