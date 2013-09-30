# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.ahappydeal.com/Type_Android+Phones~Features_3G/cell-phones-mobiles-c-59.html?freeship=f&sortby=conversion&page_size=60&24h_ship=f&display=l&newpage=1'))

serials = Array.new
vendors = Array.new
models = Array.new
prices = Array.new
url = 'ahappydeal.com'
 
doc.css('p.plist_title a').each do |serial|
  puts serial.content 
  serials << serial.content
  vendor = serial.content.split[0]
  vendors << vendor
  model = serial.content.split[1]
  models <<  model
end

doc.css('span.my_shop_price').each do |price|
  puts price.content 
  prices << price.content
end

(0..serials.length - 1).each do |index|
  listing = {
    serial: serials[index],
    vendor: vendors[index],
    model: models[index],
    url: url,
    price: prices[index]
  }
  ScraperWiki::save_sqlite(['serial'], listing)

end# Blank Ruby

# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.ahappydeal.com/Type_Android+Phones~Features_3G/cell-phones-mobiles-c-59.html?freeship=f&sortby=conversion&page_size=60&24h_ship=f&display=l&newpage=1'))

serials = Array.new
vendors = Array.new
models = Array.new
prices = Array.new
url = 'ahappydeal.com'
 
doc.css('p.plist_title a').each do |serial|
  puts serial.content 
  serials << serial.content
  vendor = serial.content.split[0]
  vendors << vendor
  model = serial.content.split[1]
  models <<  model
end

doc.css('span.my_shop_price').each do |price|
  puts price.content 
  prices << price.content
end

(0..serials.length - 1).each do |index|
  listing = {
    serial: serials[index],
    vendor: vendors[index],
    model: models[index],
    url: url,
    price: prices[index]
  }
  ScraperWiki::save_sqlite(['serial'], listing)

end# Blank Ruby

