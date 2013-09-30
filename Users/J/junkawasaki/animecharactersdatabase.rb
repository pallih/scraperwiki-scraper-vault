# scraper from anime characters database

require 'nokogiri'

html = ScraperWiki.scrape("http://www.animecharactersdatabase.com/character.php?id=1")           

doc = Nokogiri::HTML(html)

puts doc

for v in doc.css("h1.frameheader")
  puts v[0].inner_html.to_json
end
# scraper from anime characters database

require 'nokogiri'

html = ScraperWiki.scrape("http://www.animecharactersdatabase.com/character.php?id=1")           

doc = Nokogiri::HTML(html)

puts doc

for v in doc.css("h1.frameheader")
  puts v[0].inner_html.to_json
end
