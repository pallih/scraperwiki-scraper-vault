# Blank Python
#sourcescraper = 'mahon_tribunal'
import scraperwiki
scraperwiki.sqlite.attach("mahon_tribunal")
data = scraperwiki.sqlite.select('''* from mahon_tribunal.swdata order by id desc limit 10''')
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
#sourcescraper = 'mahon_tribunal'
import scraperwiki
scraperwiki.sqlite.attach("mahon_tribunal")
data = scraperwiki.sqlite.select('''* from mahon_tribunal.swdata order by id desc limit 10''')
print "<table>"
print "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data:
  print "<tr>"
  print "<td>", d["id"], "</td>"
  print "<td>", d["text"], "</td>"
  print "<td>", d["from_user"], "</td>"
  print "</tr>"
  print "</table>"
