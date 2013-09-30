###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.madingley.org/uploaded/'

# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Artist', 'Album', 'Released', 'Sales'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('table.data tr').map{|x| x.css('td')}.reject{ |x| x.length == 0}.map do |row|
    record = {}
    record['Artist']    = row[0].inner_text
    record['Album']     = row[1].inner_text
    record['Released']  = row[2].inner_text
    record['Sales'] = row[4].inner_text
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save(["Artist"], record)
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    next_link = page.at_css('a.next')
    if next_link 
      puts next_link
      next_url = BASE_URL + next_link['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 'example_table_1.html'
scrape_and_look_for_next_link(starting_url)###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.madingley.org/uploaded/'

# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Artist', 'Album', 'Released', 'Sales'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('table.data tr').map{|x| x.css('td')}.reject{ |x| x.length == 0}.map do |row|
    record = {}
    record['Artist']    = row[0].inner_text
    record['Album']     = row[1].inner_text
    record['Released']  = row[2].inner_text
    record['Sales'] = row[4].inner_text
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save(["Artist"], record)
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    next_link = page.at_css('a.next')
    if next_link 
      puts next_link
      next_url = BASE_URL + next_link['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 'example_table_1.html'
scrape_and_look_for_next_link(starting_url)