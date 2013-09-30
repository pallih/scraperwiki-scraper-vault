# Blank Python
sourcescraper = ''
print "This is a <em>fragment</em> of HTML."

import scraperwiki
scraperwiki.sqlite.attach("tutorial_36")

data = scraperwiki.sqlite.select(
    '''* from tutorial_36.swdata 
    where years_in_school > '16' order by years_in_school desc limit 10'''
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
sourcescraper = ''
print "This is a <em>fragment</em> of HTML."

import scraperwiki
scraperwiki.sqlite.attach("tutorial_36")

data = scraperwiki.sqlite.select(
    '''* from tutorial_36.swdata 
    where years_in_school > '16' order by years_in_school desc limit 10'''
)
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


