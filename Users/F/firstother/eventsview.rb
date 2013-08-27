# Blank Ruby
sourcescraper = 'events'

ScraperWiki::attach('events', 'src')  

data = ScraperWiki::select(           
  "* from src.swdata order by pubdate"
)
print "<table>"           
print "<tr><th>Title</th><th>Description</th><th>Pubdate</th></tr>"
for d in data
  print "<tr>"
    print "<td><a href='", d["link"], "'>", d["title"], "</a></td>"
    print "<td>", d["description"], "</td>"
    print "<td>", d["pubdate"].to_s, "</td>"
  print "</tr>"
end
print "</table>"