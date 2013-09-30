# Blank Ruby
require 'nokogiri'
 html = ScraperWiki::scrape("http://www.atkhairy.com/tour/photos")
 doc = Nokogiri::HTML(html)
 data = []
 doc.css('.photo_container').each do |c|
   e = {
   :link => "http://www.atkhairy.com" + c.at_css('.photo_holder a')['href'],
   :photo => c.at_css('img')['src'],
   :title => c.at_css('a').content,
   :date => c.at_css('.photo_date').content
  }
  data << e
end

ScraperWiki::save_sqlite([:link], data)
# Blank Ruby
require 'nokogiri'
 html = ScraperWiki::scrape("http://www.atkhairy.com/tour/photos")
 doc = Nokogiri::HTML(html)
 data = []
 doc.css('.photo_container').each do |c|
   e = {
   :link => "http://www.atkhairy.com" + c.at_css('.photo_holder a')['href'],
   :photo => c.at_css('img')['src'],
   :title => c.at_css('a').content,
   :date => c.at_css('.photo_date').content
  }
  data << e
end

ScraperWiki::save_sqlite([:link], data)
