import scraperwiki
scraperwiki.sqlite.attach("gho_test_1")
data = scraperwiki.sqlite.select('''* from swdata''')
print "<h1>Life expectancy at birth (Years)</h1>"
print "<table>"
print "<thead><tr><th>Country</th><th>Year</th><th>Life expectancy</th></tr></thead>"
for d in data:
  print "<tr>"
  print "<td>", d["Country"], "</td>"
  print "<td>", d["Year"], "</td>"
  print "<td>", d["Display Value"], "</td>"
  print "</tr>"
print "</table>"
