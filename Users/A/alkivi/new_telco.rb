# Blank Ruby
require 'nokogiri'
require 'open-uri'

url = "http://en.wikipedia.org/wiki/List_of_telephone_operating_companies"

data = Nokogiri::HTML(open(url))

listings = data.css('li > a:nth-child(1)')

nostart = true

count = 0

listings.each do |listing|
  if listing.text == "Zimbabwe"  
    nostart = false 
    next
  end
  next if nostart
  # next if listing.children.text == "edit"
  break if listing.text == "Fixed phone" 
  break if count > 100   
  attr = listing.attributes
  company = {
    operator: listing.text,
   # child: listing.children.text,
    link: attr["href"].value
   # title: attr["title"].value
  }
  count = count + 1

#end

  ScraperWiki::save_sqlite(['operator'], company)

end
