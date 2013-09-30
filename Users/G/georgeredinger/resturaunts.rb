require 'nokogiri'
require 'pp'
base_url='http://www.opentable.com'
resturant_list_url="/toronto-ontario-restaurant-listings"

doc = Nokogiri::HTML(ScraperWiki.scrape(base_url+resturant_list_url))

restaurants  = doc.css(".rinfo")

restaurants.each do |r|
  name = r.css('.r').text
  place,cusine=r.css('.d').text.split('|')
  resturant_url = r.css('a').attr('href').value
  #print "\"#{name}\",\"#{place}\",\"#{cusine}\","
  doc = Nokogiri::HTML(ScraperWiki.scrape("#{base_url}/#{resturant_url}"))
  email = doc.css("#RestaurantProfile_RestaurantProfileInfo_lblEmail").text.sub('Email: ','').strip
 phone = doc.css("#RestaurantProfile_RestaurantProfileInfo_lblPhone").text.sub('Phone: ','').strip

  #puts "\"#{email.text.sub('Email: ','').strip}\""
  pp ScraperWiki.save_sqlite(unique_keys=["name"],data={"name"=>name, "place"=>place, "cusine"=>cusine,"email"=>email,"phone"=>phone})
end


require 'nokogiri'
require 'pp'
base_url='http://www.opentable.com'
resturant_list_url="/toronto-ontario-restaurant-listings"

doc = Nokogiri::HTML(ScraperWiki.scrape(base_url+resturant_list_url))

restaurants  = doc.css(".rinfo")

restaurants.each do |r|
  name = r.css('.r').text
  place,cusine=r.css('.d').text.split('|')
  resturant_url = r.css('a').attr('href').value
  #print "\"#{name}\",\"#{place}\",\"#{cusine}\","
  doc = Nokogiri::HTML(ScraperWiki.scrape("#{base_url}/#{resturant_url}"))
  email = doc.css("#RestaurantProfile_RestaurantProfileInfo_lblEmail").text.sub('Email: ','').strip
 phone = doc.css("#RestaurantProfile_RestaurantProfileInfo_lblPhone").text.sub('Phone: ','').strip

  #puts "\"#{email.text.sub('Email: ','').strip}\""
  pp ScraperWiki.save_sqlite(unique_keys=["name"],data={"name"=>name, "place"=>place, "cusine"=>cusine,"email"=>email,"phone"=>phone})
end


