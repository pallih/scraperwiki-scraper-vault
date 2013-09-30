require 'rubygems' 
require 'nokogiri' 
require 'open-uri' 


doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/category/0?lang=en"))
doc.xpath('//span/a').each do |node|
puts node.text
 

end

ScraperWiki.save(['data'], {'data' => node.text})

require 'rubygems' 
require 'nokogiri' 
require 'open-uri' 


doc = Nokogiri::HTML(open("http://appworld.blackberry.com/webstore/category/0?lang=en"))
doc.xpath('//span/a').each do |node|
puts node.text
 

end

ScraperWiki.save(['data'], {'data' => node.text})

