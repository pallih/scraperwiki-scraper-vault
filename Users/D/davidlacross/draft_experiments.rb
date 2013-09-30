# Blank Ruby
require 'nokogiri' 

html = ScraperWiki::scrape("http://draftmag.com/new/reviews/")
        
page = Nokogiri::HTML html      

puts page.xpath('//*[@id="column_center"]/div[2]/div[2]').css('div.review_set')[1].text

# Blank Ruby
require 'nokogiri' 

html = ScraperWiki::scrape("http://draftmag.com/new/reviews/")
        
page = Nokogiri::HTML html      

puts page.xpath('//*[@id="column_center"]/div[2]/div[2]').css('div.review_set')[1].text

