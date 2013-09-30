require 'nokogiri'

# The link to the URL containing the data. LevelTypeId is 13 - signifying that we want to return
# local authorities and AreaId is 276693, the ID for England.
data_url = 'http://neighbourhood.statistics.gov.uk/NDE2/Disco/GetAreaAtLevel?LevelTypeId=13&AreaId=276693'

# Scrape the data.
data = ScraperWiki.scrape data_url

# Extract the scraped data from XML.
# Based upon http://nokogiri.org/
doc = Nokogiri::XML.parse(data)

# Get the data we need from the xml.
areas = doc.css('ns2|GetAreaAtLevelResponseElement Areas').children

# For each local authority...
areas.each do |area|
  # Get the name and Area ID of the LA.
  name = area.css('Name').children.first.to_s
  area_id = area.css('AreaId').children.first.to_s

  # Generate a record from the LA.
  data = {
    'area_id' => area_id,
    'name' => name
  }
  puts data

  # Save the local authority in the datastore
  ScraperWiki.save_sqlite unique_keys = ['area_id'], data = data
endrequire 'nokogiri'

# The link to the URL containing the data. LevelTypeId is 13 - signifying that we want to return
# local authorities and AreaId is 276693, the ID for England.
data_url = 'http://neighbourhood.statistics.gov.uk/NDE2/Disco/GetAreaAtLevel?LevelTypeId=13&AreaId=276693'

# Scrape the data.
data = ScraperWiki.scrape data_url

# Extract the scraped data from XML.
# Based upon http://nokogiri.org/
doc = Nokogiri::XML.parse(data)

# Get the data we need from the xml.
areas = doc.css('ns2|GetAreaAtLevelResponseElement Areas').children

# For each local authority...
areas.each do |area|
  # Get the name and Area ID of the LA.
  name = area.css('Name').children.first.to_s
  area_id = area.css('AreaId').children.first.to_s

  # Generate a record from the LA.
  data = {
    'area_id' => area_id,
    'name' => name
  }
  puts data

  # Save the local authority in the datastore
  ScraperWiki.save_sqlite unique_keys = ['area_id'], data = data
end