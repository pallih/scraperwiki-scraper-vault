sourcescraper = 'hello_world_11'

import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(
    '''* from hello_world_11.swdata 
    order by years_in_school desc limit 10'''
)

print "<table>"
print "<tr><th>Country</th><th>Years in school</th></tr>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"sourcescraper = 'hello_world_11'

import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(
    '''* from hello_world_11.swdata 
    order by years_in_school desc limit 10'''
)

print "<table>"
print "<tr><th>Country</th><th>Years in school</th></tr>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"