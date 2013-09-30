# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://liverpool.gov.uk/planning-and-building-control/search-and-track-current-applications/weekly-lists/")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

press_notices = doc.search("div.contentIntro")

puts press_notices

press_notices.search('a').each do |a|
    url = "http://liverpool.gov.uk" + a[:href]
    ScraperWiki.save_sqlite(unique_keys=["URL"], data={"URL"=>url})
end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

#doc.search('td').each do |td|
#    ScraperWiki.save(['data'], {'data' => td.inner_html})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://liverpool.gov.uk/planning-and-building-control/search-and-track-current-applications/weekly-lists/")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

press_notices = doc.search("div.contentIntro")

puts press_notices

press_notices.search('a').each do |a|
    url = "http://liverpool.gov.uk" + a[:href]
    ScraperWiki.save_sqlite(unique_keys=["URL"], data={"URL"=>url})
end

# Then we can store this data in the datastore. Uncomment the following three lines and run
# the scraper again.

#doc.search('td').each do |td|
#    ScraperWiki.save(['data'], {'data' => td.inner_html})
#end

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.