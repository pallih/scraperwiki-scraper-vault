require 'nokogiri'           

html = ScraperWiki::scrape("http://adoptioncurve.net/edms.html")           

doc = Nokogiri::HTML html

puts doc

