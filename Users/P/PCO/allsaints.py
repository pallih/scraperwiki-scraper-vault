import scraperwiki

url = 'http://allsaintswd.org.uk/services'
html = scraperwiki.scrape(url)

import lxml.html
root = lxml.html.fromstring(html)

# find table immediately after a paragraph
block = root.cssselect('p+table[class=dataTable] tr')
# extract table header row
header = []
for e in block[0].cssselect("th"):
    header.append(e.text_content().rstrip('\n'))
header[2] = 'All_Saints'
print header
# extract table body rows
for i in range(1, len(block)):
    r = {}
    for k, e in enumerate(block[i].cssselect("td")):
        r[header[k]] = e.text_content().rstrip('\n')
    scraperwiki.sqlite.save(unique_keys=[header[0]], data=r)

sourcescraper = "AllSaints"
limit = 20
offset = 0
# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print 'keys', keys
print 'rows', rows




