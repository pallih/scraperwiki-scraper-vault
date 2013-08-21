# Blank Ruby
require 'nokogiri'
require 'open-uri'

i = 1

doc = Nokogiri::HTML(open('http://www.parliament.bg/bg/MP'))
doc.xpath('//div[@class="MProw"]').each do |element|
  ScraperWiki::save_sqlite(unique_keys=['id'], data={ "id"=> i, "name" => element.content })
  i += 1
end
