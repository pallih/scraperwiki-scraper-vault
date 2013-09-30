# Blank Python
sourcescraper = 'tutorial_python_get_from_un_site'

import scraperwiki
scraperwiki.sqlite.attach("tutorial_python_get_from_un_site")
data = scraperwiki.sqlite.select(
    '''* from tutorial_python_get_from_un_site.swdata 
    order by years_in_school desc limit 20'''
)
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"

# Blank Python
sourcescraper = 'tutorial_python_get_from_un_site'

import scraperwiki
scraperwiki.sqlite.attach("tutorial_python_get_from_un_site")
data = scraperwiki.sqlite.select(
    '''* from tutorial_python_get_from_un_site.swdata 
    order by years_in_school desc limit 20'''
)
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"

