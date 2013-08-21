# Blank Python
print "This is a <em>fragment</em> of HTML."
import scraperwiki
scraperwiki.sqlite.attach("facebook_usage_guardian")

sourcescraper = 'facebook_usage_guardian'
data = scraperwiki.sqlite.select(
    '''* from facebook_usage_guardian.swdata 
    order by Percentage desc limit 50'''
)

print "<table>"
print "<tr><th>Country</th><th>Percentage</th><th>population</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Country"], "</td>"
    print "<td>", d["Percentage"], "</td>"
    print "<td>", d["population"], "</td>"
    print "</tr>"
print "</table>"
