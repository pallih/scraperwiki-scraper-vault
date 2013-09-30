###############################################################################
# SKLEP.SFD.PL Scraper 
# Get each products in store current price
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.sfd.pl/sklep/'

# scrape function: gets passed an individual page to scrape
def scrape(page)
  data_table = page.css('table.ttable tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    id = row.at_css('td.opis_td .link1')
    if id
      record = {
        ID: row.at_css('td.opis_td .link1')['href'].scan(/^.+(opis)(\d+)(\.html)$/).first[1],
        Product: row.css('td.opis_td .link1').inner_text + ' ' + row.css('td.opis_td').children[3].inner_text,
        Price: row.css('span.cena span.price').inner_text
      }
  
      # Print out the data we've gathered
      p record
  
      # Finally, save the record to the datastore - 'Product' is our unique key
      ScraperWiki.save_sqlite([:Product], record)
    end
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape(page)
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
scrape_and_look_for_next_link('http://www.sfd.pl/sklep/Aminokwasy-k105.html')###############################################################################
# SKLEP.SFD.PL Scraper 
# Get each products in store current price
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.sfd.pl/sklep/'

# scrape function: gets passed an individual page to scrape
def scrape(page)
  data_table = page.css('table.ttable tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    id = row.at_css('td.opis_td .link1')
    if id
      record = {
        ID: row.at_css('td.opis_td .link1')['href'].scan(/^.+(opis)(\d+)(\.html)$/).first[1],
        Product: row.css('td.opis_td .link1').inner_text + ' ' + row.css('td.opis_td').children[3].inner_text,
        Price: row.css('span.cena span.price').inner_text
      }
  
      # Print out the data we've gathered
      p record
  
      # Finally, save the record to the datastore - 'Product' is our unique key
      ScraperWiki.save_sqlite([:Product], record)
    end
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape(page)
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
scrape_and_look_for_next_link('http://www.sfd.pl/sklep/Aminokwasy-k105.html')