# Blank Ruby
require 'nokogiri'
require 'open-uri'

url = "http://www.930.com/concerts/#/930/"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.
# concerts = data.css('.list-view')
concerts = data.css('.list-view-item')

concerts.each do |concert|
  #prix = concert.at_css('.price')
  #if !prix.nil? 
   # prix: prix.text
  #else
   # prix: "SOLD OUT"
  #end
  listing = {
    event: concert.at_css('.headliners.summary').text,
    date: concert.at_css('.dates').text,
    doors: concert.at_css('.times').text,
    price: concert.at_css('.price-range').text
  }

#end

  ScraperWiki::save_sqlite(['event'], listing)

end
# Blank Ruby
require 'nokogiri'
require 'open-uri'

url = "http://www.930.com/concerts/#/930/"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.
# concerts = data.css('.list-view')
concerts = data.css('.list-view-item')

concerts.each do |concert|
  #prix = concert.at_css('.price')
  #if !prix.nil? 
   # prix: prix.text
  #else
   # prix: "SOLD OUT"
  #end
  listing = {
    event: concert.at_css('.headliners.summary').text,
    date: concert.at_css('.dates').text,
    doors: concert.at_css('.times').text,
    price: concert.at_css('.price-range').text
  }

#end

  ScraperWiki::save_sqlite(['event'], listing)

end
