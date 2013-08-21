sourcescraper = 'veritas-roster'

offset = 0

keys = ScraperWiki.getKeys(sourcescraper)
keys.sort()  # alphabetically

puts "<h2>Some data from scraper: #{sourcescraper}  (#{keys.length} columns)</h2>"
puts "<table border='1' style='border-collapse:collapse;'>"

limit = keys.length

puts "<tr>"
  puts "<th>Name</th><th>URL</th>"
puts "</tr>"

# rows
ScraperWiki.getData(sourcescraper, limit, offset).each do |row|
  toon_name = row['name']
  next if toon_name.nil? || toon_name == '' || toon_name == 'Nothing found.'
  puts "<tr>"
puts "<td>#{row['name']}</td><td><a href='http://us.battle.net/#{row['url']}achievement'>Achievement</a></td>"
  puts "</tr>"
end
    
puts "</table>"

#http://us.battle.net/wow/en/character/earthen-ring/tailorpinke/achievement
