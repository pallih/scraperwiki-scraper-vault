# Yusuf1
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "YUSUF"

limit = 10
offset = 0

keys = ['Name', 'Admin', 'Cp 1991-11-26',]
keys.sort()  # alphabetically

print "<h2>Principal Cities</h2>"
print '<table border="1" style="border-collapse:collapse;text-align:Left;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,

# rows
for row in getData(sourcescraper, limit, offset):
    print "<tr>",
            
print "</table>"
