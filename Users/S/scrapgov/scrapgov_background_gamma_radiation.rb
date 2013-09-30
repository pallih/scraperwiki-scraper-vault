# Blank Ruby
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open('http://www.ncrrp.org'))
doc.xpath('//span[@class="mesurment-text-color"]').each do |element|
  puts element.content
  ScraperWiki::save_sqlite(unique_keys=['id'], data={ "id"=> "gamma", "date" => Time.now, "value" => element.content })
end

# Blank Ruby
require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML(open('http://www.ncrrp.org'))
doc.xpath('//span[@class="mesurment-text-color"]').each do |element|
  puts element.content
  ScraperWiki::save_sqlite(unique_keys=['id'], data={ "id"=> "gamma", "date" => Time.now, "value" => element.content })
end

