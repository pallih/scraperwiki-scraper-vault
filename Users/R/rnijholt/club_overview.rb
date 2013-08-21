# Blank Ruby
sourcescraper = 'fpl_1'

ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select(           
    "* from club order by overall"
)
puts "<table>"           
puts "<tr><th>Attack</th><th>Defence</th><th>Overall</th><th>Name</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["attack"].to_s, "</td>"
  puts "<td>", d["defence"].to_s, "</td>"
  puts "<td>", d["overall"].to_s, "</td>"
  puts "<td>", d["name"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"
