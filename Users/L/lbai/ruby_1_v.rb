# Blank Ruby
sourcescraper = 'ruby_1'
limit = 10

ScraperWiki::attach(sourcescraper, "src")
data = ScraperWiki::sqliteexecute("select * from src.swdata order by years_in_school desc limit ?", [limit])
keys = data["keys"]
rows = data["data"]

p '<h2>Some data: ' + sourcescraper + ' (' + keys.size.to_s + ' columns)</h2>'
p '<table border="1" style="border-collapse:collapse;">'

#column headings
print "<tr>"
keys.each do |key|
  puts"<th>#{key}</th>"
end

puts "</tr>"

#rows
rows.each do |row|
  puts "<tr>"
  row.each do |value|
    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end

puts "</table>"
# Blank Ruby
sourcescraper = 'ruby_1'
limit = 10

ScraperWiki::attach(sourcescraper, "src")
data = ScraperWiki::sqliteexecute("select * from src.swdata order by years_in_school desc limit ?", [limit])
keys = data["keys"]
rows = data["data"]

p '<h2>Some data: ' + sourcescraper + ' (' + keys.size.to_s + ' columns)</h2>'
p '<table border="1" style="border-collapse:collapse;">'

#column headings
print "<tr>"
keys.each do |key|
  puts"<th>#{key}</th>"
end

puts "</tr>"

#rows
rows.each do |row|
  puts "<tr>"
  row.each do |value|
    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end

puts "</table>"
