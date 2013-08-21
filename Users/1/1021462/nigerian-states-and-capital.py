# YUSUF NADABO CHANCHANGI

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "nigeria-states-and-population"

limit = 30
offset = 0

keys = ['State','Capital']

print '<h2>Nigeria-states-and-capitals</h2>'
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in getData(sourcescraper, limit, offset):
    print "<tr>",
    for key in keys:
        print "<td>%s</td>" % row.get(key),
    print "</tr>"
    
print "</table>"
