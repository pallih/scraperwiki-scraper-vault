#

puts "This is a <em>fragment</em> of HTML."

sourcescraper = "google_trends_ja"
today = Date.today
#yesterday = today -1
yesterday = today -2

# connect to the source database giving it the name src
ScraperWiki.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
swdata = ScraperWiki.sqliteexecute("select keyword,uri from src.swdata where date = ?", [yesterday.to_s])
puts swdata

keys = swdata["keys"]
rows = swdata["data"]

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


print '<h2>Google trends on ' + yesterday.to_s + ' </h2>'

print '<table border="1" style="border-collapse:collapse;">'
rows.each do |row|
  uri = row[1]
  keyword = row[0]

  if uri == "http://"
    print '<tr><td>' + keyword + '</td></tr>'
  else
    print '<tr><td><a href=' + uri + '>' + keyword + '</a></td></tr>'
  end

end
print '</table>'

