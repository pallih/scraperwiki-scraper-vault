require 'open-uri'
require 'nokogiri'
 
doc = Nokogiri::HTML(open("http://www.mysupermarket.co.uk/departments/Biscuits_in_Sainsburys.html"))
puts doc.at_css("title").text  

doc.css(".ProductPanel").each do |product|
 puts product.css("#ProductNameLabel").text.sub(/\([^)]+\)/,'')
 puts product.css("#ProductNameLabel").text[/\(([^)]*)/,1]
 puts product.css("#PriceLabel").text
 puts product.css("#ProductPpuLabel").text

 puts product.css(".DataTable").text
end