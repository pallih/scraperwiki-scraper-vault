# Blank Ruby

p "Hello, coding in the cloud!"           

html = ScraperWiki::scrape("http://www.hemnet.se/till-salu/villa-radhus")           

require 'nokogiri'           

doc = Nokogiri::HTML html
doc.search("html body p.description a").each do |v|
  puts v
end# Blank Ruby

p "Hello, coding in the cloud!"           

html = ScraperWiki::scrape("http://www.hemnet.se/till-salu/villa-radhus")           

require 'nokogiri'           

doc = Nokogiri::HTML html
doc.search("html body p.description a").each do |v|
  puts v
end