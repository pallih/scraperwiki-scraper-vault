###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page.  We use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.skates.co.uk/scooters/maddgearpro-nitro-extreme-orange-black-scooter.html'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('table.data tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    record = {
      Product: row.css('h1')[0].inner_text,
      Price: row.css('.details_price_now_main')[1].inner_text,
      Description: row.css('details_right')[2].inner_text,
      :'Sales (m)' => row.css('td')[4].inner_text
    }

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:Product], record)
  end
end

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css('a.next')
  if next_link 
    p next_link
    next_url = BASE_URL + next_link['href']
    p next_url
    scrape_and_look_for_next_link(next_url)
  end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 'example_table_1.html'
scrape_and_look_for_next_link(starting_url)