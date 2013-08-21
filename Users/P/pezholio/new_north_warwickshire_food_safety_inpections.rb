require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'json'
require 'yaml'

id = "317"

doc = Nokogiri::XML open("http://ratings.food.gov.uk/OpenDataFiles/FHRS#{id}en-GB.xml")

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
    details[:date] = Date.parse(i["RatingDate"])
    details[:name] = i["BusinessName"]
    details[:link] = "http://ratings.food.gov.uk/business/en-GB/#{details[:id]}"
    address = [i["AddressLine1"], i["AddressLine2"], i["AddressLine3"], i["AddressLine4"], i["PostCode"]].compact.reject { |s| s.empty? }
    details[:address] = address.join(", ")
    details[:postcode] = i["PostCode"]
    details[:rating] = i["RatingValue"]
    details[:type] = i["BusinessType"]
    details[:rss_date] = details[:date].strftime("%A, %d %b %Y %H:%M:%S %Z")
    details[:lat] = i["lat"].to_f
    details[:lng] = i["lng"].to_f
    
    ScraperWiki.save(["id"], details)
end