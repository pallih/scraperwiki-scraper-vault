# Blank Python
print "This is a <em>fragment</em> of HTML."

import scraperwiki
scraperwiki.sqlite.attach("scrapertutorial_uneducationdata")
data = scraperwiki.sqlite.select(
    '''* from scrapertutorial_uneducationdata.swdata 
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
print "This is a <em>fragment</em> of HTML."

import scraperwiki
scraperwiki.sqlite.attach("scrapertutorial_uneducationdata")
data = scraperwiki.sqlite.select(
    '''* from scrapertutorial_uneducationdata.swdata 
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

