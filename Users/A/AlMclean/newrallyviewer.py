# Blank Python
sourcescraper = 'RallyResults'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''* from rallyresults.swdata 
    order by DriverName''')

print "<table>"
print "<tr><th>Driver Name</th><th>Time</th>"
for d in data:
    print "<tr>"
    print "<td>", d["DriverName"], "</td>"
    print "<td>", d["TimeString"], "</td>"
    print "</tr>"
print "</table>"

fastestData = scraperwiki.sqlite.select(''' * from rallyresults.swdata 
    order by TimeInSeconds limit 5''')

print "<table>"
print "<tr><th>Top 5 Drivers</th><th>Time</th>"
for d in fastestData:
    print "<tr>"
    print "<td>", d["DriverName"], "</td>"
    print "<td>", d["TimeString"], "</td>"
    print "</tr>"
print "</table>"

slowestData = scraperwiki.sqlite.select(''' * from rallyresults.swdata 
    order by TimeInSeconds desc limit 5''')

print "<table>"
print "<tr><th>Bottom 5 Drivers</th><th>Time</th>"
for d in slowestData :
    print "<tr>"
    print "<td>", d["DriverName"], "</td>"
    print "<td>", d["TimeString"], "</td>"
    print "</tr>"
print "</table>"

carTypes = scraperwiki.sqlite.select(''' distinct CarType from rallyresults.swdata''')

print "<table>"
print "<tr><th>Car Types featured</th>"
for d in carTypes :
    print "<tr>"
    print "<td>", d["CarType"], "</td>"
    print "</tr>"
print "</table>"