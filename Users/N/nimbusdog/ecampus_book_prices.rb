require 'nokogiri'
require 'open-uri'

@categories = ["beauty", "birthday", "clothing", "department-stores", "electronics", "flowers", "gas", "grocery", "health", "home-and-garden", "movie-tickets", "restaurants", "shoes", "travel"]
@categories.each do |category|
puts category


url = "http://www.giftcardgranny.com/category/" + category + "/"
doc = Nokogiri::HTML open(url)
doc.search( "//div[@class='title']" ).each do |store|
  name = store.inner_text.strip.gsub(" Gift Cards","")
  #puts category + "|" + name
data = {
    store: name,
    category: category
  }
  puts data.to_json
  ScraperWiki::save_sqlite(['store','category'], data)        
end
end 