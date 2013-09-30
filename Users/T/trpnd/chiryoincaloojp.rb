# Download HTML from the web
html = ScraperWiki::scrape("http://chiryoin.caloo.jp/places/search/all/k1")           

# Parsing the HTML to get your content
require 'nokogiri'           
doc = Nokogiri::HTML html
doc.search("section").each do |v|
  puts v
  cells = v.search("h3/a")
  data = {
    name: cells[0].inner_html
#    years_in_school: cells[4].inner_html.to_i
  }
#  puts data.to_json
  ScraperWiki::save_sqlite(['name'], data)
end# Download HTML from the web
html = ScraperWiki::scrape("http://chiryoin.caloo.jp/places/search/all/k1")           

# Parsing the HTML to get your content
require 'nokogiri'           
doc = Nokogiri::HTML html
doc.search("section").each do |v|
  puts v
  cells = v.search("h3/a")
  data = {
    name: cells[0].inner_html
#    years_in_school: cells[4].inner_html.to_i
  }
#  puts data.to_json
  ScraperWiki::save_sqlite(['name'], data)
end