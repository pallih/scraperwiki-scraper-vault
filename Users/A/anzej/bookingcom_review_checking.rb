# Blank Ruby
require 'date'
require 'nokogiri'   

html = ScraperWiki.scrape("http://www.booking.com/hotel/si/azul-near-ljubljana-airport.en.html")
   
doc = Nokogiri::HTML(html)

#puts doc.search('h6 span a strong.count').inner_html
reviewstoday = doc.search('h6 span a strong.count').inner_html.to_i   
today = Time.new.strftime("%Y-%m-%d")
#today = "2011-10-28"
#reviewstoday = 28
puts reviewstoday  
ScraperWiki.save_sqlite(unique_keys=["Date"], data={"Date"=>today, "Nr.of Reviews"=>reviewstoday})


# Blank Ruby
require 'date'
require 'nokogiri'   

html = ScraperWiki.scrape("http://www.booking.com/hotel/si/azul-near-ljubljana-airport.en.html")
   
doc = Nokogiri::HTML(html)

#puts doc.search('h6 span a strong.count').inner_html
reviewstoday = doc.search('h6 span a strong.count').inner_html.to_i   
today = Time.new.strftime("%Y-%m-%d")
#today = "2011-10-28"
#reviewstoday = 28
puts reviewstoday  
ScraperWiki.save_sqlite(unique_keys=["Date"], data={"Date"=>today, "Nr.of Reviews"=>reviewstoday})


