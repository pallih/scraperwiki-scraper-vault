# Blank Ruby
require 'nokogiri' 

html = ScraperWiki::scrape("http://xkcd.com") 

doc = Nokogiri::HTML html 
img = doc.search("#comic img")
ctitle = doc.search("#ctitle")
middlecontainer = doc.search("#middleContainer")
link = /http:\/\/xkcd.com\/\d+\//.match(middlecontainer.children[8].text)
xkcd_data = {
    link: link,
    ctitle: ctitle.first.text,
    image: img.first.attributes['src'].value,
    alt: img.first.attributes['title'].value
}
puts xkcd_data
ScraperWiki::save(unique_keys=['link'], data=xkcd_data)
# Blank Ruby
require 'nokogiri' 

html = ScraperWiki::scrape("http://xkcd.com") 

doc = Nokogiri::HTML html 
img = doc.search("#comic img")
ctitle = doc.search("#ctitle")
middlecontainer = doc.search("#middleContainer")
link = /http:\/\/xkcd.com\/\d+\//.match(middlecontainer.children[8].text)
xkcd_data = {
    link: link,
    ctitle: ctitle.first.text,
    image: img.first.attributes['src'].value,
    alt: img.first.attributes['title'].value
}
puts xkcd_data
ScraperWiki::save(unique_keys=['link'], data=xkcd_data)
