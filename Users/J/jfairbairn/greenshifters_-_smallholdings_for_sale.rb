require 'nokogiri'
require 'net/http'
require 'open-uri'
require 'set'

BASE_URL = 'http://www.greenshifters.co.uk/for_sale'
FOUND_URLS = Set.new

# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Title', 'URL', 'Country','Location', 'Price'])

STUFF = /[£\,]/

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('#item-showhtmllist tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    record = {}
    cells = row.css('td')
    record['Title']    = cells[2].inner_text.strip
    record['URL']     = BASE_URL + '/' + cells[2].css('a')[0]['href']
    FOUND_URLS << record['URL']
    record['Price']  = cells[4].inner_text.gsub(STUFF,'').strip.to_i
    loc = cells[3].inner_text.split(',').map(&:strip)
    record['Location'] = loc[0..-2].join(', ')
    record['Country'] = loc.last
    ScraperWiki.save_sqlite(unique_keys=["URL"], data=record)
  end
end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(ScraperWiki.scrape(url))
    scrape_table(page)
    next_link = page.at_css('.pager img[title=next]')
    return nil unless next_link
    #p next_link.parent['href']
    'http://www.greenshifters.co.uk/' + next_link.parent['href']
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL

x=scrape_and_look_for_next_link(starting_url)
while x
  x=scrape_and_look_for_next_link(x)
end

urls_in_db = ScraperWiki.select('URL from swdata').map{|i|i['URL']}

p urls_in_db

if urls_in_db
  urls_in_db.each do |url|
    next unless url
    ScraperWiki.sqliteexecute('delete from swdata where URL=?', [url]) unless FOUND_URLS.member?(url)
  end
end

