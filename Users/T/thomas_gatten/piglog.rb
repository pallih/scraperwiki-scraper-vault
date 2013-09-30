require 'rubygems'
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/newest/"))
doc.xpath('//span/a').each do |node|
puts node.text

ScraperWiki.save(['data'], {'data' => node.text})


end
require 'rubygems'
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/newest/"))
doc.xpath('//span/a').each do |node|
puts node.text

ScraperWiki.save(['data'], {'data' => node.text})


end
