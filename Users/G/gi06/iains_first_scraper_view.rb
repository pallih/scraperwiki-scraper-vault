# Blank Ruby
sourcescraper = 'iains_first_scraper'
ScraperWiki.attach("iains_first_scraper")
data = ScraperWiki.select(
    "* from iains_first_scraper.swdata 
    order by years_in_school desc limit 15"
)
#puts data
puts "<table>"
puts "<tr><th align=left>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td align=right>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"


# Blank Ruby
sourcescraper = 'iains_first_scraper'
ScraperWiki.attach("iains_first_scraper")
data = ScraperWiki.select(
    "* from iains_first_scraper.swdata 
    order by years_in_school desc limit 15"
)
#puts data
puts "<table>"
puts "<tr><th align=left>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td align=right>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"


