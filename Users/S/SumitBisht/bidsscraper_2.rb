require 'nokogiri'
require 'open-uri'

html = ScraperWiki.scrape("http://www.quibids.com")

doc = Nokogiri::HTML(open('http://www.quibids.com'))
doc.xpath("//div[@class='endinng-auction']").each do |card|
    puts card.content
    
end



