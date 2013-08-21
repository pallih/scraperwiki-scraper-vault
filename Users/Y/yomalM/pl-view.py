
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "pl" #Data table

limit = 100#Number of records
offset = 0

keys = getKeys(sourcescraper)
#keys.sort()  # alphabetically

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))
print '<table border="4" style="border-collapse:collapse;">'

print "<tr>",#This scetion interprets column headings
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"


for row in getData(sourcescraper, limit, offset):#This section interpret rows
    print "<tr>",
    for key in keys:
        print "<td>%s</td>" % row.get(key),
    print "</tr>"
    
print "</table>"
