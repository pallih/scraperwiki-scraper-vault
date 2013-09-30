require 'nokogiri'

# Attach ourselves to the scraper with the list of LAs.
ScraperWiki.attach("local_authorities_in_england")

# Get all LAs.
las = ScraperWiki.select("* from local_authorities_in_england.swdata")

# Get the record we need to start from.
last_saved = ScraperWiki.get_var 'last_saved'

puts "Starting from #{last_saved}"

# For each LA...
las[last_saved..las.size].each_with_index do |la, index|
  # Get the name and AreaID
  name = la['name']
  area_id = la['area_id']

  # Generate a URL to get the crime data from.
  url =
    "http://neighbourhood.statistics.gov.uk/NDE2/Deli/getChildAreaTables?ParentAreaId=#{area_id}&LevelTypeId=141&Datasets=2307"

  # Get the data from the URL, and parse it as xml.
  doc = Nokogiri::XML.parse ScraperWiki.scrape(url)
  # Remove all namespaces from the doc - one seems to be declared invalidly and is messing things up.
  doc.remove_namespaces!

  # Get the relevant section of the doc.
  relevant_data = doc.css('getDataCubeResponseElement Datasets Dataset')

  # Find the topic with title "Crime Score".
  topic = relevant_data.xpath("//Topics//Topic[TopicMetadata//Title='Crime Score']")
  # Get the topic ID we need to find data for.
  topic_id = topic.css('TopicId').children.first.to_s

  # Initialise an array to score the crime scores in.
  crime_scores = []

  # For each dataset item that is for the crime score...
  relevant_data.xpath("//DatasetItems//DatasetItem[TopicId=#{topic_id}]").each do |item|
    # Add the new crime score to the array of crime scores.
    crime_scores << item.css('Value').children.first.to_s.to_f
  end

  # Calculate the average crime score and add four to it (we don't want negative
  # crime scores).
  # Copied from http://stackoverflow.com/questions/1341271/average-from-a-ruby-array
  crime_score = (crime_scores.inject{ |sum, el| sum + el }.to_f / crime_scores.size)

  # If crime_scores is empty, set crime_score to 0 
  crime_score = 0 if crime_scores.empty? 

  # Create a hash to store the LA data in with some basic data.
  data = {
    'area_id' => area_id,
    'name' => name,
    'crime_score' => crime_score
  }

  # Add the data to the SW datastore.
  ScraperWiki.save_sqlite unique_keys = ['area_id'], data = data

  # Update the last_saved variable so we can resume from here.
  ScraperWiki.save_var 'last_saved', index + last_saved
endrequire 'nokogiri'

# Attach ourselves to the scraper with the list of LAs.
ScraperWiki.attach("local_authorities_in_england")

# Get all LAs.
las = ScraperWiki.select("* from local_authorities_in_england.swdata")

# Get the record we need to start from.
last_saved = ScraperWiki.get_var 'last_saved'

puts "Starting from #{last_saved}"

# For each LA...
las[last_saved..las.size].each_with_index do |la, index|
  # Get the name and AreaID
  name = la['name']
  area_id = la['area_id']

  # Generate a URL to get the crime data from.
  url =
    "http://neighbourhood.statistics.gov.uk/NDE2/Deli/getChildAreaTables?ParentAreaId=#{area_id}&LevelTypeId=141&Datasets=2307"

  # Get the data from the URL, and parse it as xml.
  doc = Nokogiri::XML.parse ScraperWiki.scrape(url)
  # Remove all namespaces from the doc - one seems to be declared invalidly and is messing things up.
  doc.remove_namespaces!

  # Get the relevant section of the doc.
  relevant_data = doc.css('getDataCubeResponseElement Datasets Dataset')

  # Find the topic with title "Crime Score".
  topic = relevant_data.xpath("//Topics//Topic[TopicMetadata//Title='Crime Score']")
  # Get the topic ID we need to find data for.
  topic_id = topic.css('TopicId').children.first.to_s

  # Initialise an array to score the crime scores in.
  crime_scores = []

  # For each dataset item that is for the crime score...
  relevant_data.xpath("//DatasetItems//DatasetItem[TopicId=#{topic_id}]").each do |item|
    # Add the new crime score to the array of crime scores.
    crime_scores << item.css('Value').children.first.to_s.to_f
  end

  # Calculate the average crime score and add four to it (we don't want negative
  # crime scores).
  # Copied from http://stackoverflow.com/questions/1341271/average-from-a-ruby-array
  crime_score = (crime_scores.inject{ |sum, el| sum + el }.to_f / crime_scores.size)

  # If crime_scores is empty, set crime_score to 0 
  crime_score = 0 if crime_scores.empty? 

  # Create a hash to store the LA data in with some basic data.
  data = {
    'area_id' => area_id,
    'name' => name,
    'crime_score' => crime_score
  }

  # Add the data to the SW datastore.
  ScraperWiki.save_sqlite unique_keys = ['area_id'], data = data

  # Update the last_saved variable so we can resume from here.
  ScraperWiki.save_var 'last_saved', index + last_saved
end