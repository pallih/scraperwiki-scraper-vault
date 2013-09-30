# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.industrialfansdirect.com/IND-FA-WH-F.html'))
 
prices = Array.new
serials = Array.new
descriptions = Array.new
 
doc.css('div > b').each do |price|
  if price.content.split(" ")[0] == "Only"  
    puts price.content 
    prices << price.content
  end
end

doc.css('div > b').each do |serial|
  if serial.content.split(" ")[0] != "Only" and serial.content.index("-") == 2  
    puts serial.content 
    serials << serial.content
 end
end

doc.css('td > a').each do |description|
  puts description.content
  descriptions << description.content
end

(0..prices.length - 1).each do |index|
  listing = {
    serial: serials[index],
    price: prices[index],   
    description: descriptions[index]
  }
  ScraperWiki::save_sqlite(['serial'], listing)

end


# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.industrialfansdirect.com/IND-FA-WH-F.html'))
 
prices = Array.new
serials = Array.new
descriptions = Array.new
 
doc.css('div > b').each do |price|
  if price.content.split(" ")[0] == "Only"  
    puts price.content 
    prices << price.content
  end
end

doc.css('div > b').each do |serial|
  if serial.content.split(" ")[0] != "Only" and serial.content.index("-") == 2  
    puts serial.content 
    serials << serial.content
 end
end

doc.css('td > a').each do |description|
  puts description.content
  descriptions << description.content
end

(0..prices.length - 1).each do |index|
  listing = {
    serial: serials[index],
    price: prices[index],   
    description: descriptions[index]
  }
  ScraperWiki::save_sqlite(['serial'], listing)

end


