require 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

BASE_URL = 'http://www.waverley.gov.uk'

agent = Mechanize.new

('a'..'z').each do |letter|
  url = BASE_URL + "/directory/3/a_to_z/#{letter}"

  page = agent.get(url)

  sites = page.search('.list li a')

  sites.each do |site|

    details = {}
    details[:name] = site.inner_text
    details[:url] = BASE_URL + site[:href]

    page = agent.get(details[:url])

    details_hash = page.search('.serviceDetails table tr').inject({}){|hsh,tr| hsh[tr.search('th')[0].inner_text.strip] = tr.search('td')[0].inner_text ;hsh }

    details[:address] = details_hash['Address']
    details[:types] = details_hash['What can you recycle here?'].gsub("\r\n", ', ')
    latlng = page.search('#map_marker_location_22')[0][:value].split(',')
    details[:lat] = latlng[0]
    details[:lng] = latlng[1]

    ScraperWiki.save([:url], details)

  end

end