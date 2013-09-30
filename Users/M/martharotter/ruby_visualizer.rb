# Blank Ruby
ScraperWiki.attach("leinster_rugby")

data = ScraperWiki.select("* from leinster_rugby.swdata order by id desc limit 10")

puts "<table>"           
puts "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data
    puts "<tr>"
    puts "<td>", d["id"], "</td>"
    puts "<td>", d["text"], "</td>"
    puts "<td>", d["from_user"], "</td>"
    puts "</tr>"
end
puts "</table>"

# Blank Ruby
ScraperWiki.attach("leinster_rugby")

data = ScraperWiki.select("* from leinster_rugby.swdata order by id desc limit 10")

puts "<table>"           
puts "<tr><th>ID</th><th>Tweet</th><th>User</th>"
for d in data
    puts "<tr>"
    puts "<td>", d["id"], "</td>"
    puts "<td>", d["text"], "</td>"
    puts "<td>", d["from_user"], "</td>"
    puts "</tr>"
end
puts "</table>"

