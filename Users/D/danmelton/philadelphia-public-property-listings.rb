###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'


# retrieve a page
starting_url = 'http://www.phila.gov/publicproperty/listings/default.aspx?pg='
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML.parse(html)

# get the number of pages
num_of_pages = doc.search('span#ctl00_bodyContent_lblTotalPages').inner_html.gsub!('Total Pages: ','').to_i
puts num_of_pages.class
num_of_pages.times do |x|
  url = starting_url + "#{x+1}"
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.search('table#ctl00_bodyContent_tblResults_dlInventoryList table').each do |td|
   if td.css('div.columnAddress').inner_html != 'Address'
      record = {"address" => td.css('div.columnAddress').inner_html, "zipcode" => td.css('div.columnZipCode').inner_html, "landsize" => td.css('div.columnLandSize').inner_html }
      ScraperWiki.save(['address'], record)
    end
  end
end


