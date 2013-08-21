# Author: Michael Sobotka
# Purpose: Fetches (german) cd-reviews from www.laut.de
# Usage: 
# 1: Go to https://scraperwiki.com/scrapers/new/ruby# 
# 2: Copy the code
# 3: Press 'Run'

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.laut.de/'

def scrape(url)
  
  # parse the url using Nokogiri HTML parser (http://nokogiri.org/)
  current_page = Nokogiri::HTML(open(url))
  
  # select all divs representing a cd
  cds = current_page.css('#alben .scrolltop.elemente8.homemedium')

  # iterate over all cds to collect information
  cds.each do |cd|

    # create a record to store the information
    record = {
      Artist: cd.css('div.artikelText h3 a span.h4')[0].inner_text[0..-3],
      Album:  cd.css('div.artikelText h3 a span.h3.h3stark')[0].inner_text,
      Teaser: cd.css('div.artikelText p.teaser')[0].inner_text.strip,
      Review: ''
    }

    # follow the details_link to get the actual review of the cd
    details_link = BASE_URL + cd.at_css('div.artikelText h3 a')['href']
    review = fetch_cd_review(details_link)

    # add the Review to the record
    record[:Review] = review

    # save the complete record into a SQLite database
    ScraperWiki::save_sqlite(['Artist', 'Album'], record)

    # print the record on the console
    p record
  end
end


def fetch_cd_review(url)
  detail_page = Nokogiri::HTML(open(url))
  
  # fetch the the cd-review
  leadtext = detail_page.css('p.leadtext')[0].inner_text.strip
  fulltext = detail_page.css('div.volltext')[0].inner_text.strip

  return (leadtext + fulltext)
end

# Start scraping...
scrape(BASE_URL)
