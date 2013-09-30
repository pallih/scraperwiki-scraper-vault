import scraperwiki           

source_scraper = 'kooples_duffle_coat_price'

scraperwiki.sqlite.attach(source_scraper)

data = scraperwiki.sqlite.select('* from %s.swdata' % source_scraper)

print "<table>"
print "<tr><th>URL</th><th>Product Name</th><th>Product Price</th><th>Product Special Price</th></tr>"
for d in data:
    print "<tr>"
    print "<td>%s</td>" % d["url"]
    print "<td>%s</td>" % d["product_name"]
    print "<td>%s</td>" % d["product_price"]
    print "<td>%s</td>" % d["product_price_special"]
    print "</tr>"
print "</table>"import scraperwiki           

source_scraper = 'kooples_duffle_coat_price'

scraperwiki.sqlite.attach(source_scraper)

data = scraperwiki.sqlite.select('* from %s.swdata' % source_scraper)

print "<table>"
print "<tr><th>URL</th><th>Product Name</th><th>Product Price</th><th>Product Special Price</th></tr>"
for d in data:
    print "<tr>"
    print "<td>%s</td>" % d["url"]
    print "<td>%s</td>" % d["product_name"]
    print "<td>%s</td>" % d["product_price"]
    print "<td>%s</td>" % d["product_price_special"]
    print "</tr>"
print "</table>"