# Scraper for Member List of Republican Study Committee
# stores the name, url and date the scraper runs for each member listed.
# the date can be used to check for people who are newly listed or 
# have left the RSC.
results = []
require 'nokogiri'
html = ScraperWiki.scrape("http://rsc.jordan.house.gov/AboutRSC/Members/")
doc = Nokogiri::HTML(html)
doc.css('td a').each do |link|
  results << {'person' => link.children.text, 'url' => link["href"], 'date' => Date.today }
end
ScraperWiki.save_sqlite(['person', 'url', 'date'], results)
# Scraper for Member List of Republican Study Committee
# stores the name, url and date the scraper runs for each member listed.
# the date can be used to check for people who are newly listed or 
# have left the RSC.
results = []
require 'nokogiri'
html = ScraperWiki.scrape("http://rsc.jordan.house.gov/AboutRSC/Members/")
doc = Nokogiri::HTML(html)
doc.css('td a').each do |link|
  results << {'person' => link.children.text, 'url' => link["href"], 'date' => Date.today }
end
ScraperWiki.save_sqlite(['person', 'url', 'date'], results)
