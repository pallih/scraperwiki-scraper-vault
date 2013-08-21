# Booking.com review scraper

require 'date'
require 'nokogiri'
require 'open-uri'

url_base = "http://www.booking.com"
properties = ["jardinvilliersp", "le-turenne","lerelaisdevellinus"]

property_prefix = "/hotel/fr/"
property_suffix = ".fr.html"

properties.each do |property|

  html = ScraperWiki.scrape(url_base + property_prefix + property + property_suffix)

  doc = Nokogiri::HTML(html)

  reviews_today = doc.search('span.score_from_number_of_reviews strong.count').inner_html.to_i   
  today = Time.new.strftime("%Y-%m-%d")

  ScraperWiki.save_sqlite(unique_keys=["Property"], data={ "Property"=>property, "Date"=>today, "Nr.of Reviews"=>reviews_today})

end
