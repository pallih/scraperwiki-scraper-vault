# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.lahinchsurfshop.com/")

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

data = {}

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.css('#feature_surfReport').each do |surf_report|
    ScraperWiki.save(['data'], {'data' => surf_report.css('h5')[0].inner_html})
ScraperWiki.save(['data'], {'data' => 'surf_report.css(\'h5\')[0].inner_html'})
    puts surf_report.css('h5')[0].inner_html
end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.





# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.