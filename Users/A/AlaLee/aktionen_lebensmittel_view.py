# Blank Python
sourcescraper = ''

import scraperwiki
scraperwiki.sqlite.attach("aktionen_lebensmittel")
data = scraperwiki.sqlite.select(
    '''* from `swdata` limit 200 '''
)



print "<table border='1'>"
print "<tr><th>Markt</th><th>Bezeichnung</th><th>Beschreibung</th><th>Bild</th><th>Preis</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Markt"], "</td>"
    print "<td>", d["Bezeichnung"], "</td>"
    print "<td>", d["Beschreibung"], "</td>"
    print "<td><a href='",d["Link"],"' target='_blank'><img src=",d["Bild"], "alt='Zielpunkt Aktionen'></a></td>"
    print "<td>", d["Preis"], "</td>"
    print "</tr>"

print "</table>"
