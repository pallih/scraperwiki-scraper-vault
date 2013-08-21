# Blank Ruby
sourcescraper = 'fpl_1'

ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select(           
    "* from player order by total_points, club, surname asc"
)
puts "<table>"           
puts "<tr><th>Firstname</th><th>Surname</th><th>Club</th><th>Position</th><th>Total Points</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["forename"].to_s, "</td>"
  puts "<td>", d["surname"].to_s, "</td>"
  puts "<td>", d["club"].to_s, "</td>"
  puts "<td>", d["position"].to_s, "</td>"
  puts "<td>", d["total_points"].to_i, "</td>"
  puts "</tr>"
end
puts "</table>"

