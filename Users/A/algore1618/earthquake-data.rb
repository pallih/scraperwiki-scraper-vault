# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

#puts html

require 'nokogiri'
require 'kernel'


arr = Array.new

for i in [1,2,3]
puts i
end




html = ScraperWiki.scrape("http://earthquake.usgs.gov/earthquakes/eqinthenews/2009/")
doc = Nokogiri::HTML(html)
arr = doc.xpath('//a[@class="eqinthenews"]').map { |link| link['href'] }
puts arr


#doc.search('a').each do |pip|
 #   ScraperWiki.save(['data'], {'data' => pip})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

#puts html

require 'nokogiri'
require 'kernel'


arr = Array.new

for i in [1,2,3]
puts i
end




html = ScraperWiki.scrape("http://earthquake.usgs.gov/earthquakes/eqinthenews/2009/")
doc = Nokogiri::HTML(html)
arr = doc.xpath('//a[@class="eqinthenews"]').map { |link| link['href'] }
puts arr


#doc.search('a').each do |pip|
 #   ScraperWiki.save(['data'], {'data' => pip})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.