# Blank Ruby
sourcescraper = 'tutorial_1_3'
puts "This is a <em>fragment</em> of HTML."
ScraperWiki.attach("tutorial_1_3")
data = ScraperWiki.select(
    "* from tutorial_1_3.swdata 
    order by years_in_school desc limit 10"
)
puts data
puts "<table>"           
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"

