require 'rubygems'
require 'nokogiri'
require 'open-uri'



HEADERS = ["photo", "title", "price", "quantity", "availible", "ends"]

DIAPER_NAMES = ["bububebe", "elemental", "lil joeys", "rumparooz", "bright star baby", "crankypants"]

start_url = "http://hyenacart.com/stores/Spots_corner/index.php?title=1&desc=1&tags=1&allnot=&category=0&u=&submit=Search&all="

def parse_file url, search_terms
  results = []
  search_terms.each do |search_term|
    search_term.gsub!(/\s/,"+")
    full_search = url + search_term
    doc = Nokogiri::HTML(open(full_search))

    rows = doc.css('table.storeTable tr')
    # remove header row
    rows.shift
    rows.each do |row|
      datum = {}
      cols = row.css('td')
      HEADERS.each_with_index do |header, index|
          datum[header] = cols[index].text.strip
      end
      results << datum
    end
  end
  results
end

results = parse_file start_url, DIAPER_NAMES

results.each do |result|
  ScraperWiki.save_sqlite(HEADERS, result)
end
