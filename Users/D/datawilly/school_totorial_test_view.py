# Blank Python
sourcescraper = 'kids_in_school_test'

print "This is a <em>fragment</em> of HTML."

import scraperwiki
scraperwiki.sqlite.attach("kids_in_school_test")

data = scraperwiki.sqlite.select(
    '''* from kids_in_school_test.swdata 
    order by years_in_school desc limit 10'''
)
print data

print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"
