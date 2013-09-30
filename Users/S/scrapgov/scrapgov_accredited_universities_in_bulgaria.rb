require 'nokogiri'
require 'open-uri'

i = 0
doc = Nokogiri::HTML(open('http://www.mon.bg/left_menu/registers/vishe/registar.html'))
doc.xpath('//div[@id="content1"]/table[1]/tbody/tr').each do |tr|
   unless i == 0
     row = { "id" => i, 
             "name" => tr.children[2].content, 
             "valid_until" => tr.children[6].content, 
             "grade" => tr.children[8].content, 
             "doc" => tr.children[10].content }
     ScraperWiki::save_sqlite(unique_keys=['id'], data=row)
   end
   i+=1
end

require 'nokogiri'
require 'open-uri'

i = 0
doc = Nokogiri::HTML(open('http://www.mon.bg/left_menu/registers/vishe/registar.html'))
doc.xpath('//div[@id="content1"]/table[1]/tbody/tr').each do |tr|
   unless i == 0
     row = { "id" => i, 
             "name" => tr.children[2].content, 
             "valid_until" => tr.children[6].content, 
             "grade" => tr.children[8].content, 
             "doc" => tr.children[10].content }
     ScraperWiki::save_sqlite(unique_keys=['id'], data=row)
   end
   i+=1
end

