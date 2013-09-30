require 'nokogiri'

puts Nokogiri::VERSION_INFO

html = ScraperWiki.scrape("http://www.mumsnet.com/Talk/politics")
doc = Nokogiri::HTML(html, nil, 'utf-8')

puts html
puts doc.search("a[title='Next page']").first
puts doc.search("//a[@title='Next page']").first
puts doc.search("a[title='Print this page']").first

require 'nokogiri'

puts Nokogiri::VERSION_INFO

html = ScraperWiki.scrape("http://www.mumsnet.com/Talk/politics")
doc = Nokogiri::HTML(html, nil, 'utf-8')

puts html
puts doc.search("a[title='Next page']").first
puts doc.search("//a[@title='Next page']").first
puts doc.search("a[title='Print this page']").first

