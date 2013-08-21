# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("test_45")

data = scraperwiki.sqlite.select(           
    '''* from test_45.swdata 
    order by years_in_school desc limit 10'''
)


print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


