# Blank Ruby
puts "Hello world"
html = ScraperWiki.scrape("http://liverpool.gov.uk/council/strategies-plans-and-policies/transport-and-streets/major-highway-schemes/")
puts html
require 'nokogiri'
doc = Nokogiri::HTML(html)

str = doc.search("article.standardContentDetail").inner_html

splitOne = str.split("<h3>")

amount = splitOne.length

i = 1

while i < amount  do

getArray = splitOne[i]

splitTwo = getArray.partition("</h3>")

location = splitTwo[0]

details = splitTwo[2]

#puts location
#puts details

ScraperWiki.save_sqlite(unique_keys=["Location", "Details"], data={"Location"=>location, "Details"=>details})

i += 1

end

