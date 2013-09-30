require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

BASE_URL = 'http://www.nhs.uk'

url = BASE_URL + "/Service-Search/Accident-and-emergency-services/ws13-6yy/Results/30/-1.82836246490479/52.6803779602051/428/0?distance=25"

doc = Nokogiri.HTML(open(url))

services = doc.search('.fctitle')

services.each do |service|
  details = {}

  details[:name] = service.search('a')[0].inner_text
  details[:url] = BASE_URL + service.search('a')[0][:href]
  contact = doc.search("td[@headers='#{service[:id]} information']")
  details[:address] = contact.search('.fcaddress').inner_text.strip
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0]
  postcode = JSON.parse open("http://www.uk-postcodes.com/postcode/#{details[:postcode].gsub(' ', '').upcase}.json").read
  details[:lat] = postcode['geo']['lat']
  details[:lng] = postcode['geo']['lng']

  ScraperWiki.save([:name], details)

end
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

BASE_URL = 'http://www.nhs.uk'

url = BASE_URL + "/Service-Search/Accident-and-emergency-services/ws13-6yy/Results/30/-1.82836246490479/52.6803779602051/428/0?distance=25"

doc = Nokogiri.HTML(open(url))

services = doc.search('.fctitle')

services.each do |service|
  details = {}

  details[:name] = service.search('a')[0].inner_text
  details[:url] = BASE_URL + service.search('a')[0][:href]
  contact = doc.search("td[@headers='#{service[:id]} information']")
  details[:address] = contact.search('.fcaddress').inner_text.strip
  details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0]
  postcode = JSON.parse open("http://www.uk-postcodes.com/postcode/#{details[:postcode].gsub(' ', '').upcase}.json").read
  details[:lat] = postcode['geo']['lat']
  details[:lng] = postcode['geo']['lng']

  ScraperWiki.save([:name], details)

end
