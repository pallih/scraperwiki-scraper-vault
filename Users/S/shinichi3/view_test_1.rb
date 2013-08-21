#########################################
# Simple table of values from one scraper
#########################################

sourcescraper = "uk_party_political_donations_parsecollector"
limit = 20
offset = 0

# connect to the source database giving it the name src
ScraperWiki.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = ScraperWiki.sqliteexecute("select * from src.swdata limit ? offset ?", [limit, offset])
keys = sdata["keys"]
rows = sdata["data"]

print '<h2>Some data from scraper: ' + sourcescraper + '  (' + keys.size.to_s + ' columns)</h2>'
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>"
keys.each do |key|
  puts "<th>#{key}</th>"
end

puts "</tr>"

# rows
rows.each do |row|
  puts "<tr>"
  row.each do |value|
    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end
    
puts "</table>"
