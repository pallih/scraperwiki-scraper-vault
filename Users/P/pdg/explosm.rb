# Blank Ruby
require 'open-uri'
require 'nokogiri' 

html = open("http://www.explosm.net/comics/") 

link = html.base_uri.to_s

doc = Nokogiri::HTML html

img = doc.search("#maincontent div div div:nth-child(2) img")
explosm_data = {
    link: link,
    image: img.first.attributes['src'].value
}
puts explosm_data
ScraperWiki::save(unique_keys=['link'], data=explosm_data)

