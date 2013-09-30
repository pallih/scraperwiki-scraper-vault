# Blank Ruby
ScraperWiki.attach("icwsm_scraper_1")

data = ScraperWiki.select("* from icwsm_scraper_1.swdata order by id desc limit 10000000")

puts "<table>"           
puts "<tr><th>User</th><th>Tweet</th><th>ID</th>"
for d in data
    puts "<tr>"
    puts "<td>", d["from_user"], "</td>"
    puts "<td>", d["text"], "</td>"
    puts "<td>", d["id"], "</td>"
    puts "</tr>"
end
puts "</table>"
# Blank Ruby
ScraperWiki.attach("icwsm_scraper_1")

data = ScraperWiki.select("* from icwsm_scraper_1.swdata order by id desc limit 10000000")

puts "<table>"           
puts "<tr><th>User</th><th>Tweet</th><th>ID</th>"
for d in data
    puts "<tr>"
    puts "<td>", d["from_user"], "</td>"
    puts "<td>", d["text"], "</td>"
    puts "<td>", d["id"], "</td>"
    puts "</tr>"
end
puts "</table>"
