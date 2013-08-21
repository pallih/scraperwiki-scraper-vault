require 'rubygems'
require 'nokogiri'
require 'open-uri'


doc = Nokogiri::HTML(open("http://store.ovi.com"))
doc.xpath('//h4/ a').each do |node|
puts node.text


end

ScraperWiki.save(['data'], {'data' => doc.xpath.inner_html})
