# Blank Ruby


require 'nokogiri'
require 'open-uri'

url = "http://photography.nationalgeographic.com/photography/photo-of-the-day"
doc = Nokogiri::HTML(open(url))
#img = doc.at_xpath("id('content_top')/x:div[2]/x:a/x:img")
puts img
# Blank Ruby


require 'nokogiri'
require 'open-uri'

url = "http://photography.nationalgeographic.com/photography/photo-of-the-day"
doc = Nokogiri::HTML(open(url))
#img = doc.at_xpath("id('content_top')/x:div[2]/x:a/x:img")
puts img
