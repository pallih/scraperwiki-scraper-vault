require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.sfsu.edu/~upd/crimelog/index.html"
doc = Nokogiri::HTML(open(url))
puts doc.at_css("title").text
doc.css(".brief").each do |brief|
  puts brief.css("h3:nth-child(3) , h3:nth-child(4)").text
  puts brief.css("p:nth-child(4) , p:nth-child(5)").text
end