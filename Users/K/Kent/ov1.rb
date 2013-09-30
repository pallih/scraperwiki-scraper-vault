require 'rubygems'
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/category/1?page=2&licenseType=2&lang=en&curr=USD"))
doc.xpath('//div/ span').each do |node|
puts node.text

end

ScraperWiki.save(['data'], {'data' => node.text})
require 'rubygems'
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/category/1?page=2&licenseType=2&lang=en&curr=USD"))
doc.xpath('//div/ span').each do |node|
puts node.text

end

ScraperWiki.save(['data'], {'data' => node.text})
