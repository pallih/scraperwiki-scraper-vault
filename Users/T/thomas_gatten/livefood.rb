require 'open-uri'
require 'nokogiri'
 
doc = Nokogiri::HTML(open("http://www.livestrong.com/thedailyplate/nutrition-calories/food/sainsburys/"))
doc.xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[2]/h2/span/a[1]').each do |node|
ScraperWiki.save(['data'], {'data' => node.text})
  puts node.text
doc.xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div').each do |node|
ScraperWiki.save(['data'], {'data' => node.text})
  puts node.text
end
end
require 'open-uri'
require 'nokogiri'
 
doc = Nokogiri::HTML(open("http://www.livestrong.com/thedailyplate/nutrition-calories/food/sainsburys/"))
doc.xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[2]/h2/span/a[1]').each do |node|
ScraperWiki.save(['data'], {'data' => node.text})
  puts node.text
doc.xpath('/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div').each do |node|
ScraperWiki.save(['data'], {'data' => node.text})
  puts node.text
end
end
