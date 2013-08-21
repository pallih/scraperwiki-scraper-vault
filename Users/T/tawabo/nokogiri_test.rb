# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'

# Get a Nokogiri::HTML:Document for the page we’re interested in...
doc = Nokogiri::HTML(open('http://www.riken.jp/r-world/info/release/press/2011/110801/detail.html'))

# Do funky things with it using Nokogiri::XML::Node methods...
####
# Search for nodes by css
puts 'Title: ' + doc.css('.press_ttl').first.content
puts 'Subtitle:' + doc.css('.press_sttl').first.content


