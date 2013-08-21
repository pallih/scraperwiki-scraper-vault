# Booking.com review scraper

require 'date'
require 'nokogiri'

url_base = "http://www.booking.com"
# review_base = "/reviewlist.nl.html?cc1=nl;offset=0;sort=language_relevance;pagename="
properties = ["costabellasercotel"]
property_prefix = "/hotel/es/"
property_suffix = ".es.html"
date_range = "?checkin_monthday=3&checkin_year_month=2012-12&checkout_monthday=4&checkout_year_month=2012-12#availability_"

properties.each do |property|

  html = ScraperWiki.scrape(url_base + property_prefix + property + property_suffix + date_range)

  doc = Nokogiri::HTML(html)

  reviews_today = doc.search('h6 span a strong.count').inner_html.to_i   
  today = Time.new.strftime("%Y-%m-%d")

  ScraperWiki.save_sqlite(unique_keys=["Property"], data={ "Property"=>property, "Date"=>today, "Nr.of Reviews"=>reviews_today})

end
