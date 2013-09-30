# Blank Python
sourcescraper = 'aras_election_data_5'
import scraperwiki
scraperwiki.sqlite.attach('aras_election_data_5')
data = scraperwiki.sqlite.select(
'''* from aras_election_data_5.swdata
order by id desc limit 10'''
)
print "<table>"
print "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data:
    print "<tr>"
    print "<td>", d["id"], "</td>"
    print "<td>", d["text"], "</td>"
    print "<td>", d["from_user"], "</td>"
    print "</tr>"
print "</table>"

# Blank Python
sourcescraper = 'aras_election_data_5'
import scraperwiki
scraperwiki.sqlite.attach('aras_election_data_5')
data = scraperwiki.sqlite.select(
'''* from aras_election_data_5.swdata
order by id desc limit 10'''
)
print "<table>"
print "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data:
    print "<tr>"
    print "<td>", d["id"], "</td>"
    print "<td>", d["text"], "</td>"
    print "<td>", d["from_user"], "</td>"
    print "</tr>"
print "</table>"

