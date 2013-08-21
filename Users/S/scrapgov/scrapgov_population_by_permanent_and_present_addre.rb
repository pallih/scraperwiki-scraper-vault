# Blank Ruby
require 'nokogiri'
require 'open-uri'
require 'iconv'

iconv = Iconv.new('WINDOWS-1251', 'UTF-8')

doc = Nokogiri::HTML(open('http://www.grao.bg/tables.html'))
doc.xpath('//div[@id="section2"]/ul/li/a').each do |element|
  puts element.content
  ScraperWiki::save_sqlite(unique_keys=['id'], data={ "id"=> element.content, "date" => Time.now, "value" => element['href'], "txt" => iconv.iconv(open("http://www.grao.bg/#{element['href']}").read) })
end


