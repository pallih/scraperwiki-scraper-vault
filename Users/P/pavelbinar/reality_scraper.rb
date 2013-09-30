require 'nokogiri'
require 'open-uri'

require 'pp'

urls = []
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=1"
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=2"
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=3"

urls.each_with_index do |url,index|

  doc = Nokogiri::HTML(open(url))
  arr =  doc.css(".result").collect do |result|
    { name = (result.css(".fn").text unless result.css(".fn").nil?)  
    price: (result.css(".price").text unless result.css(".price").nil?), 
    address: (result.at_css(".address").text unless result.css(".address").nil?) }

   # ScraperWiki::save_sqlite(['price'], price: (result.css(".price").text unless result.css(".price").nil?))

  end

endrequire 'nokogiri'
require 'open-uri'

require 'pp'

urls = []
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=1"
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=2"
urls << "http://www.sreality.cz/search?category_type_cb=1&category_main_cb=1&sub[]=2&price_min=&price_max=&region=&distance=0&usable_area-min=&usable_area-max=&floor_number-min=&floor_number-max=&age=0&extension=0&sort=0&hideRegions=0&discount=-1&perPage=30&page=3"

urls.each_with_index do |url,index|

  doc = Nokogiri::HTML(open(url))
  arr =  doc.css(".result").collect do |result|
    { name = (result.css(".fn").text unless result.css(".fn").nil?)  
    price: (result.css(".price").text unless result.css(".price").nil?), 
    address: (result.at_css(".address").text unless result.css(".address").nil?) }

   # ScraperWiki::save_sqlite(['price'], price: (result.css(".price").text unless result.css(".price").nil?))

  end

end