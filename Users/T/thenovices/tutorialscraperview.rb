# Blank Ruby

ScraperWiki.attach("tutorialscraper")

data = ScraperWiki.select("* FROM tutorialscraper.swdata ORDER BY years_in_school DESC LIMIT 10")

puts "<table>"
puts "<thead><th>Country</th><th>Years in school</th></thead>"
data.each do |d|
  puts "<tr><td>#{d.inspect}</td><td></td></tr>"
end# Blank Ruby

ScraperWiki.attach("tutorialscraper")

data = ScraperWiki.select("* FROM tutorialscraper.swdata ORDER BY years_in_school DESC LIMIT 10")

puts "<table>"
puts "<thead><th>Country</th><th>Years in school</th></thead>"
data.each do |d|
  puts "<tr><td>#{d.inspect}</td><td></td></tr>"
end