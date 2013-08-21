import lxml.etree
import lxml.html
import scraperwiki

site = "http://traintimes.org.uk"
start = site + "/live/London+Liverpool+Street"

html = scraperwiki.scrape(start)
root = lxml.html.fromstring(html)

trains = set()
for el in root.cssselect('a[title="Details"]'):
    if el.text.strip() != u"\xbb":
        continue
    trains.add(el.attrib['href'])

services = {}
for train in trains:
    html = scraperwiki.scrape(site + train)
    root = lxml.html.fromstring(html)
    times = {}
    service_name = None
    for el in root.cssselect("tr"):
        row = [lxml.etree.tostring(td, method="text")
               for td in el.cssselect("td")]
        if len(row) < 4:
            continue
        if not service_name:
            service_name = row[0] + ' ' + row[1]
        times[row[1]] = row[0] + ' ' + row[2] + ' ' + row[3]
    services[service_name] = times
    break
print services




# <a style="text-decoration:none;" title="Details" href="/live/train/PAqJxfCs0PSJMXJ8p1M%23vA">»</a>
