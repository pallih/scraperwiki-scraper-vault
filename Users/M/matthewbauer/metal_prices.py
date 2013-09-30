import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.metalprices.com/index.asp")

root = lxml.html.fromstring(html)

table = root.xpath(".//table[@id='lmeunoff_lb']")[0]

rows = table.xpath("tr[th[@class='tblrowtitle']]")

for row in rows:
    metal_name = row.xpath("th[@class='tblrowtitle']/text()")[0]
    official_usd_per_lb = float(row.xpath("td[1]/text()")[0])
    change = row.xpath("td[3]/text()")[0]
    data = {'name': metal_name, 'price': official_usd_per_lb}
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.metalprices.com/index.asp")

root = lxml.html.fromstring(html)

table = root.xpath(".//table[@id='lmeunoff_lb']")[0]

rows = table.xpath("tr[th[@class='tblrowtitle']]")

for row in rows:
    metal_name = row.xpath("th[@class='tblrowtitle']/text()")[0]
    official_usd_per_lb = float(row.xpath("td[1]/text()")[0])
    change = row.xpath("td[3]/text()")[0]
    data = {'name': metal_name, 'price': official_usd_per_lb}
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)

