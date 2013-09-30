# # # # # # # # # # # # # # # # #
# Welcome to the second ScraperWiki Ruby tutorial

# BAD LINK of the page: jdbug-pro-streetv3-0-matt-black.html

html = ScraperWiki.scrape("http://www.skates.co.uk/scooters/")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(html)
# doc = Nokogiri::HTML(open("http://www.skates.co.uk/scooters/"))

# doc.search('title').each do |title|
#     puts title.inner_html
# end
doc.search('h2').each do |h2|
    puts h2.inner_html
end
# doc.css('.details_price_now').each do |price|
doc.css('.productlist_grid_price').each do |price|
    puts price.inner_html
end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

# doc.search('title').each do |title|
#     ScraperWiki.save(['data'], {'data' => title.inner_html})
# end
# doc.search('h1').each do |h1|
#     ScraperWiki.save(['data'], {'data' => h1.inner_html})
# end
# doc.css('.details_price_now').each do |price|
#     ScraperWiki.save(['data'], {'data' => price.inner_html})
# end

doc.search('h2').each do |h2|
    ScraperWiki.save(['data'], {'data' => h2.inner_html})
# end
doc.css('.productlist_grid_price').each do |price|
    ScraperWiki.save(['data'], {'data' => price.inner_html})
end
end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
# # # # # # # # # # # # # # # # #
# Welcome to the second ScraperWiki Ruby tutorial

# BAD LINK of the page: jdbug-pro-streetv3-0-matt-black.html

html = ScraperWiki.scrape("http://www.skates.co.uk/scooters/")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(html)
# doc = Nokogiri::HTML(open("http://www.skates.co.uk/scooters/"))

# doc.search('title').each do |title|
#     puts title.inner_html
# end
doc.search('h2').each do |h2|
    puts h2.inner_html
end
# doc.css('.details_price_now').each do |price|
doc.css('.productlist_grid_price').each do |price|
    puts price.inner_html
end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

# doc.search('title').each do |title|
#     ScraperWiki.save(['data'], {'data' => title.inner_html})
# end
# doc.search('h1').each do |h1|
#     ScraperWiki.save(['data'], {'data' => h1.inner_html})
# end
# doc.css('.details_price_now').each do |price|
#     ScraperWiki.save(['data'], {'data' => price.inner_html})
# end

doc.search('h2').each do |h2|
    ScraperWiki.save(['data'], {'data' => h2.inner_html})
# end
doc.css('.productlist_grid_price').each do |price|
    ScraperWiki.save(['data'], {'data' => price.inner_html})
end
end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
