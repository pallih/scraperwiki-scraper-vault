require 'nokogiri'

for i in 1..10          
  html = ScraperWiki::scrape("http://soccerdatabase.eu/player/4/")
  sleep 10
           
  #p html
  puts "Reached"
  doc = Nokogiri::HTML html
  
  doc.css('div.descriptionColumn div').each do |link|
      puts "Test"           
      #puts link.div.text
  end
end
require 'nokogiri'

for i in 1..10          
  html = ScraperWiki::scrape("http://soccerdatabase.eu/player/4/")
  sleep 10
           
  #p html
  puts "Reached"
  doc = Nokogiri::HTML html
  
  doc.css('div.descriptionColumn div').each do |link|
      puts "Test"           
      #puts link.div.text
  end
end
