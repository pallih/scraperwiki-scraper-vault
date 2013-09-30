############
#Note from creator(Yomal Mudalige)- I have been tried to change column orders,  however still it is not finalized. Hence I added prefix 'A',  'B'.etc. Thanks
#Reference - Scraperwiki Tutorial 3
##################

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import datetime #to display update time

sourcescraper = "test_pl"

limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

d= datetime.datetime.today()
print '<th><font color =black face=verdana size=2>Last Update:</th>'
print d
print '</br>'
print '</br>'
print '<th><font color=990033 face=verdana size=5>January 2011- English Premier League</th>'
print '</br>'
print '</br>'
print '<th><font color=blue face=tahoma size=3><a href="http://scraperwiki.com/views/premier-league-table-201011-view/full/">Back to Points Table</a></th>'
print '<table border="5" cellpadding="15" style="border-collapse:collapse;">'

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
############
#Note from creator(Yomal Mudalige)- I have been tried to change column orders,  however still it is not finalized. Hence I added prefix 'A',  'B'.etc. Thanks
#Reference - Scraperwiki Tutorial 3
##################

from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import datetime #to display update time

sourcescraper = "test_pl"

limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

d= datetime.datetime.today()
print '<th><font color =black face=verdana size=2>Last Update:</th>'
print d
print '</br>'
print '</br>'
print '<th><font color=990033 face=verdana size=5>January 2011- English Premier League</th>'
print '</br>'
print '</br>'
print '<th><font color=blue face=tahoma size=3><a href="http://scraperwiki.com/views/premier-league-table-201011-view/full/">Back to Points Table</a></th>'
print '<table border="5" cellpadding="15" style="border-collapse:collapse;">'

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
