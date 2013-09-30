require 'uri'
require 'json'
require 'net/http'

# Attach ourselves to the scraper with the list of MSOAs.
ScraperWiki.attach("local_authorities_in_england")

# Get all LAs.
las = ScraperWiki.select("* from local_authorities_in_england.swdata")

# Get the record we need to start from.
last_saved = ScraperWiki.get_var 'last_saved'

puts "Starting from #{last_saved}"

# For each LA...
las[last_saved..las.size].each_with_index do |la, index|
  # Store an escaped version of the LA Name.
  la_name = URI.escape "#{la['name']}, UK"

  # Output a message saying we're starting the LA.
  puts "Starting MSOA #{la['name']} ID #{la['area_id']}"

  # Generate a URL for geocoding the LA Name.
  geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=#{la_name}&sensor=false&region=uk"

  # Output a message saying we're about to start geocoding.
  puts "Starting geocoding"

  # Scrape the JSON, and parse it.
  json = JSON.parse ScraperWiki.scrape(geocode_url)

  # Output a message saying we've finished geocoding.
  puts "Stopping geocoding"

  # Store the lat/lng location of the LA.
  location = json["results"][0]["geometry"]["location"]
  lat = location["lat"]
  lng = location["lng"]

  # Generate a URL for locating the police authority from the lat/lng.
  police_url = "policeapi2.rkh.co.uk"

  # Output a message saying we're about to start getting the police force.
  puts "Starting getting police force"

  # Check for a certain LA - the police API returns a not found on this one for
  # some reason. Instead, we'll just manually list it as being in Lancashire.
  if la['area_id'] == "276913" or la['area_id'] == "276914"
    force = "cumbria"
  elsif la['area_id'] == "277018" or la['area_id'] == "276819"
    force = "lancashire"
  elsif la['area_id'] == "277070"
    force = "north-yorkshire"
  elsif la['area_id'] == "277083"
    force = "nottinghamshire"
  elsif la['area_id'] == "277148"
    force = "west-marcia"
  elsif la['area_id'] == "276748"
    force = "metropolitan"
  else
    # Connect to the URL, authenticate and store the response in a string.
    # Based upon http://ruby-doc.org/stdlib/libdoc/net/http/rdoc/classes/Net/HTTP.html

    req = Net::HTTP::Get.new "/api/locate-neighbourhood?q=#{lat},#{lng}"
    res = Net::HTTP.start(police_url) do |http|
      req.basic_auth 'nerob22', '458f4034f943f1867d090de18f18f52b'
      http.request(req)
    end
        
    # Parse the resonse as JSON and store it
    json = JSON.parse res.body
  
    # Store the force of the LA.
    force = json['force']
  end

  # Output a message saying we've finished getting the police force.
  puts "Stopping getting police force"

  # Create a new hash storing the LA details, including the police force.
  la_hash = {
    "name" => la['name'],
    "area_id" => la['area_id'],
    "force" => force
  }

  # Output a message.
  puts "Saving LA #{index}"

  # Add the row to the ScraperWiki datastore.
  ScraperWiki.save_sqlite unique_keys = ["area_id"], data = la_hash

  # Update the last_saved variable so we can resume from here.
  ScraperWiki.save_var 'last_saved', index + last_saved
endrequire 'uri'
require 'json'
require 'net/http'

# Attach ourselves to the scraper with the list of MSOAs.
ScraperWiki.attach("local_authorities_in_england")

# Get all LAs.
las = ScraperWiki.select("* from local_authorities_in_england.swdata")

# Get the record we need to start from.
last_saved = ScraperWiki.get_var 'last_saved'

puts "Starting from #{last_saved}"

# For each LA...
las[last_saved..las.size].each_with_index do |la, index|
  # Store an escaped version of the LA Name.
  la_name = URI.escape "#{la['name']}, UK"

  # Output a message saying we're starting the LA.
  puts "Starting MSOA #{la['name']} ID #{la['area_id']}"

  # Generate a URL for geocoding the LA Name.
  geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=#{la_name}&sensor=false&region=uk"

  # Output a message saying we're about to start geocoding.
  puts "Starting geocoding"

  # Scrape the JSON, and parse it.
  json = JSON.parse ScraperWiki.scrape(geocode_url)

  # Output a message saying we've finished geocoding.
  puts "Stopping geocoding"

  # Store the lat/lng location of the LA.
  location = json["results"][0]["geometry"]["location"]
  lat = location["lat"]
  lng = location["lng"]

  # Generate a URL for locating the police authority from the lat/lng.
  police_url = "policeapi2.rkh.co.uk"

  # Output a message saying we're about to start getting the police force.
  puts "Starting getting police force"

  # Check for a certain LA - the police API returns a not found on this one for
  # some reason. Instead, we'll just manually list it as being in Lancashire.
  if la['area_id'] == "276913" or la['area_id'] == "276914"
    force = "cumbria"
  elsif la['area_id'] == "277018" or la['area_id'] == "276819"
    force = "lancashire"
  elsif la['area_id'] == "277070"
    force = "north-yorkshire"
  elsif la['area_id'] == "277083"
    force = "nottinghamshire"
  elsif la['area_id'] == "277148"
    force = "west-marcia"
  elsif la['area_id'] == "276748"
    force = "metropolitan"
  else
    # Connect to the URL, authenticate and store the response in a string.
    # Based upon http://ruby-doc.org/stdlib/libdoc/net/http/rdoc/classes/Net/HTTP.html

    req = Net::HTTP::Get.new "/api/locate-neighbourhood?q=#{lat},#{lng}"
    res = Net::HTTP.start(police_url) do |http|
      req.basic_auth 'nerob22', '458f4034f943f1867d090de18f18f52b'
      http.request(req)
    end
        
    # Parse the resonse as JSON and store it
    json = JSON.parse res.body
  
    # Store the force of the LA.
    force = json['force']
  end

  # Output a message saying we've finished getting the police force.
  puts "Stopping getting police force"

  # Create a new hash storing the LA details, including the police force.
  la_hash = {
    "name" => la['name'],
    "area_id" => la['area_id'],
    "force" => force
  }

  # Output a message.
  puts "Saving LA #{index}"

  # Add the row to the ScraperWiki datastore.
  ScraperWiki.save_sqlite unique_keys = ["area_id"], data = la_hash

  # Update the last_saved variable so we can resume from here.
  ScraperWiki.save_var 'last_saved', index + last_saved
end