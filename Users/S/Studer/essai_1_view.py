# Blank Python
sourcescraper = 'essai_1'

print "This is a <em>fragment</em> of HTML." 

import scraperwiki 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( ''' * from '''+sourcescraper+'''.swdata order by years_in_school desc limit 10''' ) 

print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"
# Blank Python
sourcescraper = 'essai_1'

print "This is a <em>fragment</em> of HTML." 

import scraperwiki 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( ''' * from '''+sourcescraper+'''.swdata order by years_in_school desc limit 10''' ) 

print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"
