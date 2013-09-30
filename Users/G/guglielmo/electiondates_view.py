# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("electiondates")

data = scraperwiki.sqlite.select(           
    '''* from swdata 
    order by election_date desc limit 10'''
)


print "<table>"
print "<tr><th>Data</th><th>Regione</th><th>Provincia</th><th>Citt&agrave;</th></tr>"
for d in data:
    print "<tr>"
    print "<td>", d["election_date"], "</td>"
    print "<td>", d["prov"], "</td>"
    print "<td>", d["reg"], "</td>"
    print "<td>", d["city"], "</td>"
    print "</tr>"
print "</table>"


# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("electiondates")

data = scraperwiki.sqlite.select(           
    '''* from swdata 
    order by election_date desc limit 10'''
)


print "<table>"
print "<tr><th>Data</th><th>Regione</th><th>Provincia</th><th>Citt&agrave;</th></tr>"
for d in data:
    print "<tr>"
    print "<td>", d["election_date"], "</td>"
    print "<td>", d["prov"], "</td>"
    print "<td>", d["reg"], "</td>"
    print "<td>", d["city"], "</td>"
    print "</tr>"
print "</table>"


