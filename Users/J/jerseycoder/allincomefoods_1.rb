# Blank Ruby
#require "json"
require 'nokogiri'
require "net/http"
require "uri"

# set the return from the function (which is an array) to an array called usergeo
#usergeo = get_geo_and_zip_from_address(incomingstreetaddy,incomingcity,incomingst)
baseUrl = "http://oakland.crimespotting.org/crime-data?format=xml&bbox=-122.2777,37.7993,-122.2682,37.8077&type=theft,robbery,simple_assault&count=2"
url = URI.parse(baseUrl)
resp = Net::HTTP.get_response(url)
  fsData = Nokogiri::XML(resp.body)
  reports = fsData.xpath('//report')
  reports.each do |rep|
  status = rep.xpath("//report").text;
  puts status
end
  #feats = fsData["features"]
  #props = feats["properties"]
  #puts props
  #ScraperWiki.save(['casenumber', 'crimetype', 'datetime', 'date', 'time', 'lat', 'long', 'beat', 'link', 'crime'], #{'retailer' => tarr[0].text, 'streetaddress' => tarr[1].text, 'city' => tarr[2].text, 'state' => tarr[3].text, #'zipcode' => tarr[4].text, 'restaurant' => tarr[5].text, 'farmmkt' => tarr[6].text, 'lat' => retailergeo["lat"], #'crime' => fsData.xpath("//report").text});
  




