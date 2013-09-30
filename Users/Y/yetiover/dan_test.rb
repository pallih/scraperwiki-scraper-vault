# encoding: ISO-8859-1
require 'nokogiri'


# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://thetimes.co.uk")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

#require 'nokogiri'
#doc = Nokogiri::HTML(html)
#doc.search('title').each do |title|
#    puts title.inner_html
#end
#doc.search('h1').each do |h1|
#    puts h1.inner_html
#end
#doc.css('.details_price_now').each do |price|
#    puts price.inner_html
#end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

#doc.search('title').each do |title|
#    ScraperWiki.save(['data'], {'data' => title.inner_html})
#end
#doc.search('h1').each do |h1|
#    ScraperWiki.save(['data'], {'data' => h1.inner_html})
#end
#doc.css('.details_price_now').each do |price|
#    ScraperWiki.save(['data'], {'data' => price.inner_html})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.









# encoding: ISO-8859-1
require 'nokogiri'


# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://thetimes.co.uk")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

#require 'nokogiri'
#doc = Nokogiri::HTML(html)
#doc.search('title').each do |title|
#    puts title.inner_html
#end
#doc.search('h1').each do |h1|
#    puts h1.inner_html
#end
#doc.css('.details_price_now').each do |price|
#    puts price.inner_html
#end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

#doc.search('title').each do |title|
#    ScraperWiki.save(['data'], {'data' => title.inner_html})
#end
#doc.search('h1').each do |h1|
#    ScraperWiki.save(['data'], {'data' => h1.inner_html})
#end
#doc.css('.details_price_now').each do |price|
#    ScraperWiki.save(['data'], {'data' => price.inner_html})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.









