sourcescraper = 'test_ruby'

limit = 20
offset = 0

ScraperWiki.attach(sourcescraper)
keys = ScraperWiki.sqliteexecute('select * from `%s`.swdata limit 0' % sourcescraper)['keys']
keys.sort()  # alphabetically

puts "<h2>Some data from scraper: #{sourcescraper}  (#{keys.length} columns)</h2>"
puts "<table border='1' style='border-collapse:collapse;'>"

# column headings
puts "<tr>"
keys.each do |key|
  puts "<th>#{key}</th>"
end
puts "</tr>"

# rows
ScraperWiki.select('* from `%s`.swdata limit ? offset ?' % sourcescraper, [limit, offset]).each do |row|
    puts "<tr>"
    keys.each do |key|
      print "<td>#{row[key]}</td>"
    end
    puts "</tr>"
end
    
puts "</table>"sourcescraper = 'test_ruby'

limit = 20
offset = 0

ScraperWiki.attach(sourcescraper)
keys = ScraperWiki.sqliteexecute('select * from `%s`.swdata limit 0' % sourcescraper)['keys']
keys.sort()  # alphabetically

puts "<h2>Some data from scraper: #{sourcescraper}  (#{keys.length} columns)</h2>"
puts "<table border='1' style='border-collapse:collapse;'>"

# column headings
puts "<tr>"
keys.each do |key|
  puts "<th>#{key}</th>"
end
puts "</tr>"

# rows
ScraperWiki.select('* from `%s`.swdata limit ? offset ?' % sourcescraper, [limit, offset]).each do |row|
    puts "<tr>"
    keys.each do |key|
      print "<td>#{row[key]}</td>"
    end
    puts "</tr>"
end
    
puts "</table>"