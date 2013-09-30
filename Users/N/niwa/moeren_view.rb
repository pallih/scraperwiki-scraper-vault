# Blank Ruby
sourcescraper = 'moeren'

#puts "This is a <em>fragment</em> of HTML."


ScraperWiki.attach("moeren")
data = ScraperWiki.select(           
    "* from moeren.swdata order by file_name"
)

for d in data
  puts "<tr>"
  puts "<td><a href='", d["url"], "'>", d["file_name"], "</a></td>"
  puts "<td>", d["comment"], "</td>"
  puts "<td>", d["date"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "</tr>"
  puts "<br>"
end# Blank Ruby
sourcescraper = 'moeren'

#puts "This is a <em>fragment</em> of HTML."


ScraperWiki.attach("moeren")
data = ScraperWiki.select(           
    "* from moeren.swdata order by file_name"
)

for d in data
  puts "<tr>"
  puts "<td><a href='", d["url"], "'>", d["file_name"], "</a></td>"
  puts "<td>", d["comment"], "</td>"
  puts "<td>", d["date"], "</td>"
  puts "<td>", d["size"], "</td>"
  puts "</tr>"
  puts "<br>"
end