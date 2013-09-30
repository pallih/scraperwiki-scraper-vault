###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page.  We use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.shipspotting.com/gallery/search.php?page_limit=100&limitstart=11100&search_title=&search_title_option=1&search_imo=&search_pen_no=&search_mmsi=&search_callsign=&search_category_1=265&search_cat1childs=on&search_uid=&search_country=&search_port=&search_subports=&search_flag=&search_homeport=&search_adminstatus=&search_classsociety=&search_builder=&search_buildyear1=&search_owner=&search_manager=&sortkey=p.lid&sortorder=desc&page_limit=100&viewtype=1'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.xpath('.//center').collect do |row|

if row.at_css('.whiteboxstroke td:nth-child(1) a')
      ship = row.css('.boxHeaderfreetxt').inner_text
      imo = row.css('a:nth-child(5)').inner_text
      url = row.css('.whiteboxstroke td:nth-child(1) a')[0]['href']
else
      ship = row.css('.boxHeaderfreetxt').inner_text
      imo = row.css('a:nth-child(5)').inner_text
      url = 'unknown'
end

    record = {
      Ship: ship,
      IMO: imo,
      URL: url
    }

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:Ship], record)
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css('a#next_page_link')
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
starting_url = BASE_URL
scrape_and_look_for_next_link(starting_url)###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page.  We use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.shipspotting.com/gallery/search.php?page_limit=100&limitstart=11100&search_title=&search_title_option=1&search_imo=&search_pen_no=&search_mmsi=&search_callsign=&search_category_1=265&search_cat1childs=on&search_uid=&search_country=&search_port=&search_subports=&search_flag=&search_homeport=&search_adminstatus=&search_classsociety=&search_builder=&search_buildyear1=&search_owner=&search_manager=&sortkey=p.lid&sortorder=desc&page_limit=100&viewtype=1'

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.xpath('.//center').collect do |row|

if row.at_css('.whiteboxstroke td:nth-child(1) a')
      ship = row.css('.boxHeaderfreetxt').inner_text
      imo = row.css('a:nth-child(5)').inner_text
      url = row.css('.whiteboxstroke td:nth-child(1) a')[0]['href']
else
      ship = row.css('.boxHeaderfreetxt').inner_text
      imo = row.css('a:nth-child(5)').inner_text
      url = 'unknown'
end

    record = {
      Ship: ship,
      IMO: imo,
      URL: url
    }

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:Ship], record)
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css('a#next_page_link')
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
starting_url = BASE_URL
scrape_and_look_for_next_link(starting_url)