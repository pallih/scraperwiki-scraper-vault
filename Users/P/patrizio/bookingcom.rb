# Booking.com review scraper

require 'date'
require 'nokogiri'

url_base = "http://www.booking.com"
# review_base = "/reviewlist.nl.html?cc1=nl;offset=0;sort=language_relevance;pagename="
properties = ["stayokay-rotterdam", "stayokdenhaag", "stayokayamdamvond", "stayokay-amsterdam-zeeburg", "stayokay-valkenswaard", "stayokay-dordrecht","stayokay-bergen-op-zoom", "stayokayhostelbunnik", "stayokay-maastricht", "stayokarnhem", "stayokay-terschelling", "stayokay-sneek","stayokapeldoorn","stayokay-heemskerk", "stayokay-haarlem","stayokay-doorwerth","stayokaygrou","stayokay-noordwijk","stayokay-texel","stayokay-domburg"]
property_prefix = "/hotel/nl/"
property_suffix = ".nl.html"

properties.each do |property|

  html = ScraperWiki.scrape(url_base + property_prefix + property + property_suffix)

  doc = Nokogiri::HTML(html)

  reviews_today = doc.search('h6 span a strong.count').inner_html.to_i   
  today = Time.new.strftime("%Y-%m-%d")

  ScraperWiki.save_sqlite(unique_keys=["Property"], data={ "Property"=>property, "Date"=>today, "Nr.of Reviews"=>reviews_today})

end
# Booking.com review scraper

require 'date'
require 'nokogiri'

url_base = "http://www.booking.com"
# review_base = "/reviewlist.nl.html?cc1=nl;offset=0;sort=language_relevance;pagename="
properties = ["stayokay-rotterdam", "stayokdenhaag", "stayokayamdamvond", "stayokay-amsterdam-zeeburg", "stayokay-valkenswaard", "stayokay-dordrecht","stayokay-bergen-op-zoom", "stayokayhostelbunnik", "stayokay-maastricht", "stayokarnhem", "stayokay-terschelling", "stayokay-sneek","stayokapeldoorn","stayokay-heemskerk", "stayokay-haarlem","stayokay-doorwerth","stayokaygrou","stayokay-noordwijk","stayokay-texel","stayokay-domburg"]
property_prefix = "/hotel/nl/"
property_suffix = ".nl.html"

properties.each do |property|

  html = ScraperWiki.scrape(url_base + property_prefix + property + property_suffix)

  doc = Nokogiri::HTML(html)

  reviews_today = doc.search('h6 span a strong.count').inner_html.to_i   
  today = Time.new.strftime("%Y-%m-%d")

  ScraperWiki.save_sqlite(unique_keys=["Property"], data={ "Property"=>property, "Date"=>today, "Nr.of Reviews"=>reviews_today})

end
