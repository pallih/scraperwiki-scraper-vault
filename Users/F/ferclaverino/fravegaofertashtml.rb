puts "This is a <em>fragment</em> of HTML."
ScraperWiki::attach("fravegaofertas")

data = ScraperWiki::select(
    "* from swdata"
)
puts data

puts "<table>"
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["name"], "</td>"
  puts "<td>", d["brand"], "</td>"
  puts "</tr>"
end
puts "</table>"


