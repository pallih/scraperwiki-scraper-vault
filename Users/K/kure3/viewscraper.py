# Blank Python
sourcescraper = 'kscraper'


import scraperwiki           
scraperwiki.sqlite.attach("kscraper")

data = scraperwiki.sqlite.select(           
    '''* from kscraper.swdata 
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
# Blank Python
sourcescraper = 'kscraper'


import scraperwiki           
scraperwiki.sqlite.attach("kscraper")

data = scraperwiki.sqlite.select(           
    '''* from kscraper.swdata 
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
