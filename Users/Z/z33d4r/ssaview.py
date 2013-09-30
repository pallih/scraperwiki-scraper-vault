# Blank Python
sourcescraper = 'ssa'

import scraperwiki
scraperwiki.sqlite.attach("ssa")

data = scraperwiki.sqlite.select(
    '''* from ssa.swdata 
    order by title limit 10'''
)
print data

print "<table>"
print "<tr><th>title</th><th>d</th><th>dl</th>"
for d in data:
    print "<tr>"
    print "<td>", d["title"], "</td>"
    print "<td>", d["d"], "</td>"
    print "<td>", d["dl"], "</td>"
    print "</tr>"
print "</table>"
# Blank Python
sourcescraper = 'ssa'

import scraperwiki
scraperwiki.sqlite.attach("ssa")

data = scraperwiki.sqlite.select(
    '''* from ssa.swdata 
    order by title limit 10'''
)
print data

print "<table>"
print "<tr><th>title</th><th>d</th><th>dl</th>"
for d in data:
    print "<tr>"
    print "<td>", d["title"], "</td>"
    print "<td>", d["d"], "</td>"
    print "<td>", d["dl"], "</td>"
    print "</tr>"
print "</table>"
