###############################################################################
# CA Interpreters
###############################################################################

require 'nokogiri'
require 'open-uri'

# retrieve a page
BASE_URL  = 'http://www.yellowpages.com'
FIRST_EXT = '/ca/translators-interpreters?g=CA'

# define the order our columns are displayed in the datastore
mdc = SW_MetadataClient.new
mdc.save('data_columns', ['Business', 'Address', 'City', 'State', 'Zipcode', 'Phone']) 

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  page.css('.listing_content').collect do |x|
    record = {}
    record['Business']  = x.css('.business-name a').text
    record['Address']   = x.css('.street-address').text.sub(/,[\s]*/, '')
    record['City']      = x.css('.locality').text
    record['State']     = x.css('.region').text
    record['Zipcode']   = x.css('.postal-code').text
    record['Phone']     = x.css('.business-phone').text
    ScraperWiki.save(["Business"], record)
  end
end


#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    puts 'scraping: '+url
    scrape_table(page)
    next_link = page.at_css('li.next')
    if next_link
      next_url = BASE_URL + next_link.at_css('a').attribute("href")
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL+FIRST_EXT
scrape_and_look_for_next_link(starting_url)
