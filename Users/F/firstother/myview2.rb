# Blank Ruby
sourcescraper = 'nettimoto'

ScraperWiki::attach('nettimoto', 'src')  

data = ScraperWiki::select(           
  "* from src.swdata order by price"
)
print "<table>"           
print "<tr><th>ImgUrl</th><th>Year</th><th>Mileage</th><th>Loc</th><th>Name</th><th>Brief</th><th>Price in EUR</th><th>Near</th></tr>"
for d in data
  print "<tr>"
  print "<td><img src='", d["img_url"], "'border='0' width='154' height='115'></td>"
  print "<td>", d["year"].to_s, "</td>"
  print "<td>", d["mileage"].to_s, "</td>"
  print "<td>", d["loc"], "</td>"
  print "<td><a href='", d["url"], "'>", d["name"], "</a></td>"
  print "<td>", d["brief"], "</td>"
  print "<td>", d["price"].to_s, "</td>"
  print "<td>", d["near"].to_s, "</td>"
  print "</tr>"
end
print "</table>"