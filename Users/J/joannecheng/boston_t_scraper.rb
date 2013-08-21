# Blank Ruby
require 'scraperwiki'
require 'json'
require 'httparty'

def get_trips(line)
  url = "http://developer.mbta.com/lib/rthr/#{line}.json"
  JSON.parse(HTTParty.get(url).body)
end

puts "start"
trips = []
['red', 'blue', 'orange'].each do |line|
  get_trips(line)['TripList']['Trips'].each do |trip|
    unless trip['Position'].nil? 
      position = trip['Position'].merge 'line' => line
      trips << position
    end
  end
end
puts trips

ScraperWiki::save_sqlite(unique_keys=trips[0].keys, data=trips)