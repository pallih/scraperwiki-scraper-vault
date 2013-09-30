import scraperwiki
scraperwiki.sqlite.attach("weathergcca_week_prevision")

data = scraperwiki.sqlite.select(
    '''* from weathergcca_week_prevision.swdata
    order by date'''
)
print "<table>"           
print "<tr><th>Day</th><th>Date</th><th>Condition</th><th>Max</th><th>Min</th><th>% dePrecipitation</th>"
for d in data:
  print "<tr>"
  print "<td>", d["day"], "</td>"
  print "<td>", d["date"], "</td>"
  print "<td>", d["condition"], "</td>"
  print "<td>", d["high"], "</td>"
  print "<td>", d["low"], "</td>"
  print "<td>", d["pop"], "</td>"
  print "</tr>"
print "</table>"import scraperwiki
scraperwiki.sqlite.attach("weathergcca_week_prevision")

data = scraperwiki.sqlite.select(
    '''* from weathergcca_week_prevision.swdata
    order by date'''
)
print "<table>"           
print "<tr><th>Day</th><th>Date</th><th>Condition</th><th>Max</th><th>Min</th><th>% dePrecipitation</th>"
for d in data:
  print "<tr>"
  print "<td>", d["day"], "</td>"
  print "<td>", d["date"], "</td>"
  print "<td>", d["condition"], "</td>"
  print "<td>", d["high"], "</td>"
  print "<td>", d["low"], "</td>"
  print "<td>", d["pop"], "</td>"
  print "</tr>"
print "</table>"