#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import cgi
import os

sourcescraper = "bmw_wheel_setups"

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
body=params.get('body','Coupe')
wheel=params.get('wheel','Rear')

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata where body=? and wheel=? order by size, offset, tire, rubbing", (body, wheel))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))

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

