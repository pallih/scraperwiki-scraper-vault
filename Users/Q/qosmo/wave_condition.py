import scraperwiki
scraperwiki.sqlite.attach("wave_hunter_info")

data = scraperwiki.sqlite.select(
    '''* from wave_hunter_info.swdata 
    order by date desc limit 10'''
)

print "<table>"           
print "<tr><th>date</th><th>wave</th>"
for d in data:
    print "<tr>"
    print "<td>", d["date"], "</td>"
    print "<td>", d["wavepoint"], "</td>"
    print "</tr>"
print "</table>"