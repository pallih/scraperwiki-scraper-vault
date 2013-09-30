import scraperwiki

#get the source
scraperwiki.sqlite.attach( 'baumkunde')

#load the source (only the top 20 items ... since it's slow
data = scraperwiki.sqlite.select( '''* from baumkunde.swdata order by latin_name limit 20''' )

#print a simple table
print "<table>" 
print "<tr><th>Common name</th><th>Latin name</th><th>Origin</th><th>Notes</th>" 
for d in data: 
    print "<tr>" 
    print "<td>", d["latin_name"], "</td>"
    print "<td>", d["common_name"], "</td>"
    print "<td>", d["origin"], "</td>"
    print "<td>", d["notes"], "</td>"
    print "</tr>" 
print "</table>"
import scraperwiki

#get the source
scraperwiki.sqlite.attach( 'baumkunde')

#load the source (only the top 20 items ... since it's slow
data = scraperwiki.sqlite.select( '''* from baumkunde.swdata order by latin_name limit 20''' )

#print a simple table
print "<table>" 
print "<tr><th>Common name</th><th>Latin name</th><th>Origin</th><th>Notes</th>" 
for d in data: 
    print "<tr>" 
    print "<td>", d["latin_name"], "</td>"
    print "<td>", d["common_name"], "</td>"
    print "<td>", d["origin"], "</td>"
    print "<td>", d["notes"], "</td>"
    print "</tr>" 
print "</table>"
