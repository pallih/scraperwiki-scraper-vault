# Welcome to the second ScraperWiki Ruby tutorial.

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape "http://www.allisonmartell.com"
p html

# Next we use Nokogiri to extract the values from the HTML source.
# There should be output in the console.

require 'nokogiri'

doc = Nokogiri::HTML(html)

#doc.css('.details_price_now').each do |price|
#  p price.inner_html
#end

# Then we can store this data in the datastore. Uncomment the following blocks and run
# the scraper again.

doc.search('title').each do |title|
  ScraperWiki.save([:data], {data: title.inner_html})
end

doc.search('p').each do |p|
  ScraperWiki.save([:text], {text: p.inner_html})
end

#doc.css('.details_price_now').each do |price|
#  ScraperWiki.save([:data], {data: price.inner_html})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.