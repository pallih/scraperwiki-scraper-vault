# Blank Ruby

html = ScraperWiki.scrape(URL)
puts html

i=0

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('LI[class="close"]').each do |row|  
   puts row
   puts i.to_s()
    i=i+1
end
# Blank Ruby

html = ScraperWiki.scrape(URL)
puts html

i=0

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('LI[class="close"]').each do |row|  
   puts row
   puts i.to_s()
    i=i+1
end
# Blank Ruby

html = ScraperWiki.scrape(URL)
puts html

i=0

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
puts doc
doc.search('LI[class="close"]').each do |row|  
   puts row
   puts i.to_s()
    i=i+1
end
