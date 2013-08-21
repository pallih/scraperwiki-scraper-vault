import scraperwiki

scraperwiki.sqlite.attach("wl")
data = scraperwiki.sqlite.select("* from swdata")

print "<html><head></head><body>"
print "<table>"
print "<tr><th>Haltestelle</th><th>Ziel</th><th>Abfahrt</th>"

for d in data:
    print "<tr>"
    print "<td>", d["haltestelle"], "</td>"
    print "<td>", d["ziel"], "</td>"
    print "<td>", d["abfahrt"], "</td>"
    print "</tr>"

print "</table>"
print "</body></html>"
