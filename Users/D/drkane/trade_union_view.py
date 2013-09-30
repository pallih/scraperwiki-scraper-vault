import scraperwiki           
scraperwiki.sqlite.attach("trade-unions")
data = scraperwiki.sqlite.select(           
    '* from `trade-unions`.swdata'
)
print "<table>"           
print "<tr><th>Name</th>"
for d in data:
    print "<tr>"
    print "<td>", d["name"], "</td>"
    print "</tr>"
print "</table>"
import scraperwiki           
scraperwiki.sqlite.attach("trade-unions")
data = scraperwiki.sqlite.select(           
    '* from `trade-unions`.swdata'
)
print "<table>"           
print "<tr><th>Name</th>"
for d in data:
    print "<tr>"
    print "<td>", d["name"], "</td>"
    print "</tr>"
print "</table>"
