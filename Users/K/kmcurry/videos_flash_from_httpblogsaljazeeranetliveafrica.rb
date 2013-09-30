###############################################################################
# This scraper is a mod to Tutorial 3.  It scrapes Al Jazeera Live Blogs for
# Africa for videos. (Technically is scrapes object tags.)
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://blogs.aljazeera.net/'

# todo - make a schema.  Apparently save_metadata is deprecated
#ScraperWiki.save_metadata('data_columns', ['URL', 'Timestamp'])

# scrape function: gets passed an individual page to scrape
def scrape(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.search('object').each do |object|
    obj = object['data']
    if obj
      puts obj
      ScraperWiki.save(['URL', 'SOURCE'], {'URL' => obj, 'SOURCE' => url})
    end
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape(url)
    next_link = page.xpath(".//a[@title='Go to next page']")
    puts next_link
    if next_link && next_link[0]
      puts next_link[0]['href']
      next_url = BASE_URL + next_link[0]['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 'live/africa'
scrape_and_look_for_next_link(starting_url)###############################################################################
# This scraper is a mod to Tutorial 3.  It scrapes Al Jazeera Live Blogs for
# Africa for videos. (Technically is scrapes object tags.)
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://blogs.aljazeera.net/'

# todo - make a schema.  Apparently save_metadata is deprecated
#ScraperWiki.save_metadata('data_columns', ['URL', 'Timestamp'])

# scrape function: gets passed an individual page to scrape
def scrape(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.search('object').each do |object|
    obj = object['data']
    if obj
      puts obj
      ScraperWiki.save(['URL', 'SOURCE'], {'URL' => obj, 'SOURCE' => url})
    end
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape(url)
    next_link = page.xpath(".//a[@title='Go to next page']")
    puts next_link
    if next_link && next_link[0]
      puts next_link[0]['href']
      next_url = BASE_URL + next_link[0]['href']
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL + 'live/africa'
scrape_and_look_for_next_link(starting_url)