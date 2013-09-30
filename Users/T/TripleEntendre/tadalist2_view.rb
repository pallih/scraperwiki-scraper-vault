sourcescraper = 'tadalist2'

limit = 20
offset = 0

keys = ScraperWiki.getKeys(sourcescraper)
keys.sort()  # alphabetically

#puts "<h2>Some data from scraper: #{sourcescraper}  (#{keys.length} columns)</h2>"
#puts "<table border='1' style='border-collapse:collapse;'>"

# column headings
#puts "<tr>"
#keys.each do |key|
#  puts "<th>#{key}</th>"
#end
#puts "</tr>"

# rows
ScraperWiki.getData(sourcescraper, limit, offset).each do |row|
#    puts "<tr>"
    keys.each do |key|
      #print "<td>#{row[key]}</td>"
      #puts key
      next if key != "listhtml"
      #print "#{row[key]}"
      unless row[key].nil? 
          puts row[key]
      end
    end
#    puts "</tr>"
end

#data = ScraperWiki.getData(sourcescraper, limit, offset)

#puts data.first    

#puts "</table>"
sourcescraper = 'tadalist2'

limit = 20
offset = 0

keys = ScraperWiki.getKeys(sourcescraper)
keys.sort()  # alphabetically

#puts "<h2>Some data from scraper: #{sourcescraper}  (#{keys.length} columns)</h2>"
#puts "<table border='1' style='border-collapse:collapse;'>"

# column headings
#puts "<tr>"
#keys.each do |key|
#  puts "<th>#{key}</th>"
#end
#puts "</tr>"

# rows
ScraperWiki.getData(sourcescraper, limit, offset).each do |row|
#    puts "<tr>"
    keys.each do |key|
      #print "<td>#{row[key]}</td>"
      #puts key
      next if key != "listhtml"
      #print "#{row[key]}"
      unless row[key].nil? 
          puts row[key]
      end
    end
#    puts "</tr>"
end

#data = ScraperWiki.getData(sourcescraper, limit, offset)

#puts data.first    

#puts "</table>"
