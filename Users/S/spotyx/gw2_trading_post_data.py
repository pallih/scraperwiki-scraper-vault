import scraperwiki.sqlite
sourcescraper = 'test_gw2_items'
scraperwiki.sqlite.attach(sourcescraper, "gw2")
sdata = scraperwiki.sqlite.execute("select * from gw2.swdata")

keys = sdata.get("keys")
rows = sdata.get("data")
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"
# rows
for row in rows:
    print "<tr>",
    for value in row:
        print "<td>%s</td>" % value,
    print "</tr>"
    
print "</table>"
