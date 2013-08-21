sourcescraper = 'hackerspacesorg_-_active_labs'

puts '{"type": "FeatureCollection", "features": ['

data_string = ''
# rows
ScraperWiki.getData(sourcescraper).each do |row|
  unless row['coordinates'].nil? || row['coordinates'].empty? 
    data_string << '{"geometry": {"coordinates": ' + row['coordinates'] + ', "type": "Point"}, '
    properties = %w(profile_id website name city)
    data_string << '"properties": {'
      properties.each do |property|
      data_string << "\"#{property}\": \"#{row[property]}\""
      data_string << ", " unless property == properties.last
    end
    data_string << "}},\n"
  end
end

# remove last coma
puts data_string[0..-3] + "\n"
 
puts ']}'
