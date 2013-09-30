# Blank Python
import scraperwiki

sourcescraper = 'espn_standings'

scraperwiki.sqlite.attach("espn_standings")  

data = scraperwiki.sqlite.select(           
    '''* from espn_standings.swdata 
    order by PCT desc limit 50'''
)
         
print "<table>"           
print "<tr><th>NBA Standings</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Name"], "</td>"
    print "<td>", d["W"], "</td>"
    print "<td>", d["L"], "</td>"
    print "<td>", d["PCT"], "</td>"
    print "</tr>"
print "</table>"# Blank Python
import scraperwiki

sourcescraper = 'espn_standings'

scraperwiki.sqlite.attach("espn_standings")  

data = scraperwiki.sqlite.select(           
    '''* from espn_standings.swdata 
    order by PCT desc limit 50'''
)
         
print "<table>"           
print "<tr><th>NBA Standings</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Name"], "</td>"
    print "<td>", d["W"], "</td>"
    print "<td>", d["L"], "</td>"
    print "<td>", d["PCT"], "</td>"
    print "</tr>"
print "</table>"