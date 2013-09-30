require 'open-uri'
require 'nokogiri'

url = "http://chicago.craigslist.org/chc/apa/"


data = Nokogiri::HTML(open(url))
listings = data.search('.row')

listings.each do |listing|
  puts "Posted Date/Time: " + data.css('h4').text
  puts "Title: " + listing.css('.pl').text
  puts "Price: " + listing.css('.price').text
  puts "Neighborhoods/Location:" + listing.css('small').text
end
