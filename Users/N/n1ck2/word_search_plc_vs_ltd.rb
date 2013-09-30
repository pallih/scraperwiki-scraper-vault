# Blank Ruby

links = Array.new

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Category:Companies_based_in_Liverpool")           
puts html
#
require 'nokogiri'           

doc = Nokogiri::HTML(html)

table = doc.search("table[@width='100%']")
  
table.search('a').each do |a|
    url = "http://en.wikipedia.org" + a[:href]
    links.push(url)
end

arrayLength = links.length

i = 0

while i < arrayLength do
  
  html = ScraperWiki.scrape(links[i])           
  
  puts html
#breaks when it gets to Downing Developments, can't think why
  
  #ScraperWiki.save_sqlite(unique_keys=["Link", "Headline"], data={"Link"=>hyperlink, "Headline"=>headline})
  
  i += 1

end# Blank Ruby

links = Array.new

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Category:Companies_based_in_Liverpool")           
puts html
#
require 'nokogiri'           

doc = Nokogiri::HTML(html)

table = doc.search("table[@width='100%']")
  
table.search('a').each do |a|
    url = "http://en.wikipedia.org" + a[:href]
    links.push(url)
end

arrayLength = links.length

i = 0

while i < arrayLength do
  
  html = ScraperWiki.scrape(links[i])           
  
  puts html
#breaks when it gets to Downing Developments, can't think why
  
  #ScraperWiki.save_sqlite(unique_keys=["Link", "Headline"], data={"Link"=>hyperlink, "Headline"=>headline})
  
  i += 1

end