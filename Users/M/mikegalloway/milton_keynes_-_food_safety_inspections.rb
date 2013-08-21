# Based on template by pezholio see blog at http://bit.ly/15eqyPz
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'json'
require 'yaml'

url = "http://ratings.food.gov.uk/OpenDataFiles/FHRS870en-GB.xml"
# See blog for more details of how to find the url for a specific council 
# Both date lines below modified from template by adding rescue nil to cover situation when date is blank

doc = Nokogiri::XML open(url)

inspections = []

doc.search('EstablishmentDetail').each do |i|
   details = i.children.inject({}){|hsh,el| hsh[el.name] = el.inner_text;hsh}
   details["lat"] = i.search('Geocode Latitude').inner_text rescue nil
   details["lng"] = i.search('Geocode Longitude').inner_text rescue nil
   inspections << details
end

inspections.each do |i|
    details = {}
    details[:id] = i["FHRSID"]
    details[:councilid] = i["LocalAuthorityBusinessID"]
    details[:date] = Date.parse(i["RatingDate"]) rescue nil
    details[:name] = i["BusinessName"]
    details[:link] = "http://ratings.food.gov.uk/business/en-GB/#{details[:id]}"
    address = [i["AddressLine1"], i["AddressLine2"], i["AddressLine3"], i["AddressLine4"], i["PostCode"]].compact.reject { |s| s.empty? }
    details[:address] = address.join(", ")
    details[:postcode] = i["PostCode"]
    details[:rating] = i["RatingValue"]
    details[:type] = i["BusinessType"]
    details[:rss_date] = details[:date].strftime("%A, %d %b %Y %H:%M:%S %Z") rescue nil
    details[:lat] = i["lat"]
    details[:lng] = i["lng"]
    
    ScraperWiki.save(["id"], details)
end