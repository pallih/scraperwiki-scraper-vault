require 'nokogiri'
html = ScraperWiki.scrape("http://www.gp.se/")
doc = Nokogiri::HTML(html)

tags = doc.css('h3.richText')
tags = tags.sort
puts 'Found ' + tags.size.to_s + ' h3 tags'
tags.each do |tag|           
  puts tag.text
end
