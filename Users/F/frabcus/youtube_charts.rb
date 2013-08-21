puts "Hello, coding in the cloud!"

html = ScraperWiki.scrape("http://www.youtube.com/charts")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search('.video-details').each do |v|
  title = v.search('h3 a').first['title']
  ScraperWiki.save(unique_keys=['title'], data={'title' => title})
end


