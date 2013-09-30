# Blank Ruby
sourcescraper = 'chris ketchel'
ScraperWiki.attach("tutor2")
data = ScraperWiki.select(
    "* from tutor2.swdata 
    order by years_in_school desc limit 10"
)
puts "<table>"
puts "<tr><th>Country</th><th>Years</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"

# Blank Ruby
sourcescraper = 'chris ketchel'
ScraperWiki.attach("tutor2")
data = ScraperWiki.select(
    "* from tutor2.swdata 
    order by years_in_school desc limit 10"
)
puts "<table>"
puts "<tr><th>Country</th><th>Years</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"

