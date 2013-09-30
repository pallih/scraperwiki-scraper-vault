# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.stadtbranchenbuch.com/muenster/P/393.html")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)


# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

doc.search('.rLiTop').each do |li|
    name= doc.css('h3')
    address= doc.css('address')
#    name=  td.css("address").first.inner_html.split("</a>").map(&:'strip')
#    td.css("a").inner_html
    something = "#{data,name}"
    ScraperWiki.save(['data'], {'data' => something})
end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.stadtbranchenbuch.com/muenster/P/393.html")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)


# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

doc.search('.rLiTop').each do |li|
    name= doc.css('h3')
    address= doc.css('address')
#    name=  td.css("address").first.inner_html.split("</a>").map(&:'strip')
#    td.css("a").inner_html
    something = "#{data,name}"
    ScraperWiki.save(['data'], {'data' => something})
end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.