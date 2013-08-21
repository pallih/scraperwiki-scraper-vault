#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "dun-laoghaire-rathdown-county-council-planning-app"

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

print '<h2>Data from scraper: %s</h2>' % sourcescraper
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in getData(sourcescraper):
    print "<tr>",
    for key in keys:
        print "<td>%s</td>" % row.get(key),
    print "</tr>"
    
print "</table>"
