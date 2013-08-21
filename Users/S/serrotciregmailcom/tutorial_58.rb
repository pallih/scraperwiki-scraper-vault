# Blank Ruby

html = ScraperWiki::scrape("http://www.basspro.com/webapp/wcs/stores/servlet/Navigation?storeId=10151&catalogId=10051&langId=-1&searchTerm=waders")

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("span[@class='thumbnailPrice'] strong").each do |v|
  cells = v.search 'span'
  if cells.count == 12
    data = {
      price: cells[0].inner_html,
   #  years_in_school: cells[4].inner_html.to_i
    }
        #ScraperWiki::save_sqlite(['country'], data)
require 'pp'
pp ScraperWiki::save_sqlite(unique_keys=["price"], data)
  end
end

