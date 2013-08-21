import scraperwiki
import lxml.html           


for i in range(1, 858):
    html = scraperwiki.scrape('http://www.ksp.gov.in/home/station-details.php?station_id='+str(i))
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    print tables[7].text_content()
    row = 0
    data ={'i': i}
    for tr in (tables[7]).cssselect("tr"):
        row = row+1
        if row == 0:
            continue
        tds = tr.cssselect("td")
        if len(tds) > 1:
            data['col'+str(row)] = tds[1].text_content()
    print data
    scraperwiki.sqlite.save(unique_keys=['i'], data=data)
