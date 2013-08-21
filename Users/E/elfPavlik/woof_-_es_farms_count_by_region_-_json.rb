sourcescraper = 'wwoof_-_es'

# get data
stats = Hash.new(0) # returns 0 if value not exists

ScraperWiki.getData(sourcescraper).each do |record|
  stats[record['Province']] += 1
end

puts '['
puts stats.map{|key, value| "{\"#{key}\": #{value}}"}.join(',')
puts ']'

