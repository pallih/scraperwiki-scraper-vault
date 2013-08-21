# Правителство на РБ
require 'nokogiri'
require 'open-uri'

i = 1

doc = Nokogiri::HTML(open('http://www.government.bg/cgi-bin/e-cms/vis/vis.pl?s=001&p=0219&g='))
doc.xpath('//body/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/a/font').each do |element|
  ScraperWiki::save_sqlite(unique_keys=['id'], data={ "id"=> i, "name" => element.content.encode('UTF-8') })
  i += 1
end

