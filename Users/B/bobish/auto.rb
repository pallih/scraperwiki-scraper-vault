require 'nokogiri'
require 'mechanize'



for pa in 1..20
  puts pa
  
  html = ScraperWiki::scrape("http://www2.autotrader.co.uk/search/used/cars/postcode/sw31pt/radius/1500/maximum-mileage/up_to_20000_miles/maximum-age/up_to_2_years_old/seller-type/trade_adverts/price-from/7000/price-to/75000/onesearchad/used%2Cnearlynew%2Cnew/sort/default/page/#{pa}")
  
  doc = Nokogiri::HTML(html)

  puts doc.css('div.vehicleTitle h2#advert1advertTitleMain a.external').text

  
  
end