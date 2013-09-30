# Blank Python

import scraperwiki           
scraperwiki.sqlite.attach("wwoofbrazil")

data = scraperwiki.sqlite.select(           
    "* from wwoofbrazil.swdata where State like '%Sao Paulo%' order by City"
)
print "<table>"           
print "<tr><th>City</th><th>State</th><th>Food</th>"
for d in data:
    print "<tr>"
    print "<td>", d["City"], "</td>"
    print "<td>", d["State"], "</td>"
    print "<td>", d["Food"], "</td>"
    print "</tr>"
print "</table>"
# Blank Python

import scraperwiki           
scraperwiki.sqlite.attach("wwoofbrazil")

data = scraperwiki.sqlite.select(           
    "* from wwoofbrazil.swdata where State like '%Sao Paulo%' order by City"
)
print "<table>"           
print "<tr><th>City</th><th>State</th><th>Food</th>"
for d in data:
    print "<tr>"
    print "<td>", d["City"], "</td>"
    print "<td>", d["State"], "</td>"
    print "<td>", d["Food"], "</td>"
    print "</tr>"
print "</table>"
