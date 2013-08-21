import scraperwiki, lxml.html

url = "http://www.hidemyass.com/proxy-list/"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(unicode(html))

proxyTable = root.cssselect("table#listtable")
print proxyTable[0]
rows = proxyTable[0].cssselect("tr")

for row in rows:
    for cell in row.cssselect("td"):
        print cell.text_content()
