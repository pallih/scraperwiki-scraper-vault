###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.sportsmanager.ie/cake/gaa2/dgf/'

# define the order our columns are displayed in the datastore
#ScraperWiki.save_var('data_columns', ['Home Club', 'Away Club', 'Venue', 'Date', 'Referee', 'Comment'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  level = "No Level"
  puts 'here'
  data_table = page.css('table.fixtures tr').collect do |row|
    puts row 
    record = {}
    #puts row['class'] == competition
    if row['class'] == "competition"
      puts 'here1'
       level = row.css('td p')[0].inner_text
    elsif row['class'] == "item"
      puts 'here2'
      record['Home Club']    = row.css('td.homeClub')[0].inner_text
      record['Away Club']    = row.css('td.awayClub')[0].inner_text
      record['Venue']    = row.css('td.venue')[0].inner_text
      record['Date']    = row.css('td.time')[0].inner_text
      record['Time']    = row.css('td.time')[1].inner_text
      record['Referee']    = row.css('td.referee')[0].inner_text
      record['Comment']    = row.css('td.comment')[0].inner_text
      record['Level']    = level
    else
      # do nothing
      puts "here3"
    end
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
   # ScraperWiki.save("Game", record)
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

starting_url = BASE_URL + 'fixtures/7130/c_c_c2_fixtures'
#starting_url = BASE_URL + 'fixtures/7167/c_c_c1_fixtures'
#starting_url = BASE_URL + 'upcomingFixtures'
scrape_and_look_for_next_link(starting_url)###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.sportsmanager.ie/cake/gaa2/dgf/'

# define the order our columns are displayed in the datastore
#ScraperWiki.save_var('data_columns', ['Home Club', 'Away Club', 'Venue', 'Date', 'Referee', 'Comment'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  level = "No Level"
  puts 'here'
  data_table = page.css('table.fixtures tr').collect do |row|
    puts row 
    record = {}
    #puts row['class'] == competition
    if row['class'] == "competition"
      puts 'here1'
       level = row.css('td p')[0].inner_text
    elsif row['class'] == "item"
      puts 'here2'
      record['Home Club']    = row.css('td.homeClub')[0].inner_text
      record['Away Club']    = row.css('td.awayClub')[0].inner_text
      record['Venue']    = row.css('td.venue')[0].inner_text
      record['Date']    = row.css('td.time')[0].inner_text
      record['Time']    = row.css('td.time')[1].inner_text
      record['Referee']    = row.css('td.referee')[0].inner_text
      record['Comment']    = row.css('td.comment')[0].inner_text
      record['Level']    = level
    else
      # do nothing
      puts "here3"
    end
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
   # ScraperWiki.save("Game", record)
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

starting_url = BASE_URL + 'fixtures/7130/c_c_c2_fixtures'
#starting_url = BASE_URL + 'fixtures/7167/c_c_c1_fixtures'
#starting_url = BASE_URL + 'upcomingFixtures'
scrape_and_look_for_next_link(starting_url)