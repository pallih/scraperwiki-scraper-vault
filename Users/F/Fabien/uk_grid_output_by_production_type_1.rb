require 'rexml/document'
require 'net/http'

include REXML

def table_exists?
  !ScraperWiki::sqliteexecute("SELECT name FROM sqlite_master WHERE type='table' AND name='swdata';")['data'].empty? 
end

# Get and parse data from www.bmreports.com
url = "http://www.bmreports.com/bsp/additional/soapfunctions.php?element=generationbyfueltypetable"
xml = Net::HTTP.get_response(URI.parse(url))
doc = REXML::Document.new(xml.body)

# Initialize hash to store retrieved data
data = {}

# Add timestamp and aggregate power output
data['DATE'] = "#{doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/LAST24H/@FROM_SD"]}"
data['TOTAL'] = "#{doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/LAST24H/@TOTAL"]}"

# Add power output for each fuel type to hash
doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/INST"].each do |entry|
  data["#{REXML::XPath.first(entry,'@TYPE')}"] = "#{REXML::XPath.first(entry,'@PCT')}"
end

# do something with data

# Store in ScraperWiki
last_recorded_date = ScraperWiki::sqliteexecute("select max(DATE) from swdata limit 1") if table_exists?

unless last_recorded_date == data['DATE']
  ScraperWiki::save_sqlite(data.keys, data) 
end



require 'rexml/document'
require 'net/http'

include REXML

def table_exists?
  !ScraperWiki::sqliteexecute("SELECT name FROM sqlite_master WHERE type='table' AND name='swdata';")['data'].empty? 
end

# Get and parse data from www.bmreports.com
url = "http://www.bmreports.com/bsp/additional/soapfunctions.php?element=generationbyfueltypetable"
xml = Net::HTTP.get_response(URI.parse(url))
doc = REXML::Document.new(xml.body)

# Initialize hash to store retrieved data
data = {}

# Add timestamp and aggregate power output
data['DATE'] = "#{doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/LAST24H/@FROM_SD"]}"
data['TOTAL'] = "#{doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/LAST24H/@TOTAL"]}"

# Add power output for each fuel type to hash
doc.elements["GENERATION_BY_FUEL_TYPE_TABLE/INST"].each do |entry|
  data["#{REXML::XPath.first(entry,'@TYPE')}"] = "#{REXML::XPath.first(entry,'@PCT')}"
end

# do something with data

# Store in ScraperWiki
last_recorded_date = ScraperWiki::sqliteexecute("select max(DATE) from swdata limit 1") if table_exists?

unless last_recorded_date == data['DATE']
  ScraperWiki::save_sqlite(data.keys, data) 
end



