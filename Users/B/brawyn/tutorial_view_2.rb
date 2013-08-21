# Tutorial View

sourcescraper = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=first_scrapper_1&query=select%20*%20from%20%60swdata%60%20limit%2010'

ScraperWiki.attach("first_scrapper_1")

data = ScraperWiki.select(
    "* from first_scrapper_1.swdata 
    order by years_in_school desc limit 25"
)

puts "<table>"
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"
