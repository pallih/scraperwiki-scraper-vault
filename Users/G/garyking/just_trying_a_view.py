#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "test_81"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
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
#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "test_81"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
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
