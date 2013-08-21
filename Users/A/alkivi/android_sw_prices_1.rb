# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.superzonewholesale.com/Wholesale-mtk6577-android-phone_c1101?page=1&display=All-1&productsort=3&pagesize=200'))

serials = Array.new
vendors = Array.new
models = Array.new
prices = Array.new
url = 'superzonewholesale.com'
 
#x=doc.css('dt').children[0]
doc.css('dt').children.children.children.each do |serial|
  puts serial.text
  serials << serial.text
  vendor = serial.content.split[0]
  vendors << vendor
  model = serial.content.split[1]
  models <<  model
end

#y=doc.css('strong.red.big')[0].children
doc.css('strong.red.big').children.each do |price|
  puts price.text
  prices << price.text
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

end



