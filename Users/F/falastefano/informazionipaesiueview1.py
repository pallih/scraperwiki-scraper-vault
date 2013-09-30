import scraperwiki

#
# Informazioni sugli stati della UE / View 1
#


# 1. Query the scraper's datastore
# --------------------------------

# Before you can read the scraper's datastore from the view, you need to attach to it, using its shortname (the name in its URL).
scraperwiki.sqlite.attach("informazionistatiue")

count_paesi=-1
superficie_totale=-1
popolazione_totale=-1

# Conteggio paesi
dataTmp = scraperwiki.sqlite.select('''count(*) as conteggio from informazionistatiue.swdata order by country''')
for result in dataTmp:
    count_paesi = result['conteggio']
# Superficie totale
dataTmp = scraperwiki.sqlite.select('''sum(superficie) as superficie_totale from informazionistatiue.swdata''')
for result in dataTmp:
     superficie_totale = result['superficie_totale']
# Popolazione totale
dataTmp = scraperwiki.sqlite.select('''sum(popolazione) as popolazione_totale from informazionistatiue.swdata''')
for result in dataTmp:
     popolazione_totale = result['popolazione_totale']

# Elenco paesi con dettagli
data = scraperwiki.sqlite.select('''* from informazionistatiue.swdata order by country''')


# 2. Print out the results
# ------------------------

print "<style>.centered {text-align: center;}</style>"

print "<table>"
print "<tr>"
print "<td>"
print "Paesi della UE: ", count_paesi, "<br><br>"
print "Superficie totale della UE: ", superficie_totale, "km²<br><br>"
print "Popolazione totale della UE: ", popolazione_totale, "km²<br><br>"
print "</td>"
print '<td><iframe src="https://views.scraperwiki.com/run/paesiue-capitali-map/" width="600" height="400">Mappa</iframe>'
print "</td>"
print "</tr>"
print "</table>"

# Follows a simple example outputting HTML, but you could output a KML file, an iCal file, an RSS feed, or whatever you need.
print "<table>"
print "<tr><th>Paese</th>"
print "<th>Bandiera</th>"
#print "<th>Details</th>"
print "<th>Anno di adesione all’UE</th>"
print "<th>Capitale</th>"
print "<th>Superficie (km²)</th>"
print "<th>Popolazione <br>(milioni di abitanti)</th>"
print "<th>Valuta</th><th>Area Schenghen</th>"
print "<th>Pagina dettagli</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", '<img width="24" hspace="0" height="16" border="0" alt="',d["country"],'" src="',d["flagImageURL"],'">', "</td>"
#    print '<td width="400">', d["details"], "</td>"
    print '<td>', d["anno_adesione"], "</td>"
    print '<td>', d["capitale"], "</td>"
    print '<td class="centered">', d["superficie"], "</td>"
    print '<td class="centered">', d["popolazione"], "</td>"
    print '<td>', d["valuta"], "</td>"
    print '<td>', d["schenghen"], "</td>"
    print '<td>', '<a href="',d["detailPageURL"],'">DETAILS PAGE</a>', '</td>'
    print "</tr>"
print "</table>"

import scraperwiki

#
# Informazioni sugli stati della UE / View 1
#


# 1. Query the scraper's datastore
# --------------------------------

# Before you can read the scraper's datastore from the view, you need to attach to it, using its shortname (the name in its URL).
scraperwiki.sqlite.attach("informazionistatiue")

count_paesi=-1
superficie_totale=-1
popolazione_totale=-1

# Conteggio paesi
dataTmp = scraperwiki.sqlite.select('''count(*) as conteggio from informazionistatiue.swdata order by country''')
for result in dataTmp:
    count_paesi = result['conteggio']
# Superficie totale
dataTmp = scraperwiki.sqlite.select('''sum(superficie) as superficie_totale from informazionistatiue.swdata''')
for result in dataTmp:
     superficie_totale = result['superficie_totale']
# Popolazione totale
dataTmp = scraperwiki.sqlite.select('''sum(popolazione) as popolazione_totale from informazionistatiue.swdata''')
for result in dataTmp:
     popolazione_totale = result['popolazione_totale']

# Elenco paesi con dettagli
data = scraperwiki.sqlite.select('''* from informazionistatiue.swdata order by country''')


# 2. Print out the results
# ------------------------

print "<style>.centered {text-align: center;}</style>"

print "<table>"
print "<tr>"
print "<td>"
print "Paesi della UE: ", count_paesi, "<br><br>"
print "Superficie totale della UE: ", superficie_totale, "km²<br><br>"
print "Popolazione totale della UE: ", popolazione_totale, "km²<br><br>"
print "</td>"
print '<td><iframe src="https://views.scraperwiki.com/run/paesiue-capitali-map/" width="600" height="400">Mappa</iframe>'
print "</td>"
print "</tr>"
print "</table>"

# Follows a simple example outputting HTML, but you could output a KML file, an iCal file, an RSS feed, or whatever you need.
print "<table>"
print "<tr><th>Paese</th>"
print "<th>Bandiera</th>"
#print "<th>Details</th>"
print "<th>Anno di adesione all’UE</th>"
print "<th>Capitale</th>"
print "<th>Superficie (km²)</th>"
print "<th>Popolazione <br>(milioni di abitanti)</th>"
print "<th>Valuta</th><th>Area Schenghen</th>"
print "<th>Pagina dettagli</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", '<img width="24" hspace="0" height="16" border="0" alt="',d["country"],'" src="',d["flagImageURL"],'">', "</td>"
#    print '<td width="400">', d["details"], "</td>"
    print '<td>', d["anno_adesione"], "</td>"
    print '<td>', d["capitale"], "</td>"
    print '<td class="centered">', d["superficie"], "</td>"
    print '<td class="centered">', d["popolazione"], "</td>"
    print '<td>', d["valuta"], "</td>"
    print '<td>', d["schenghen"], "</td>"
    print '<td>', '<a href="',d["detailPageURL"],'">DETAILS PAGE</a>', '</td>'
    print "</tr>"
print "</table>"

