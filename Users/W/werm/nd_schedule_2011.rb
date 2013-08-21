html = ScraperWiki.scrape("http://www.und.com/sports/m-footbl/sched/nd-m-footbl-sched.html")           
puts html

require 'rubygems'  
require 'nokogiri'  
require 'open-uri' 
require 'mechanize'

doc = Nokogiri::HTML(html)

row = doc.xpath("//*[(@id = 'schedtable')]")

unless row == nil
date = row.css(".row-text:nth-child(1)")
opponent = row.css(".row-text:nth-child(2)")
location = row.css(".row-text:nth-child(3)")
result = row.css(".row-text:nth-child(4)")

puts date.inner_html
puts opponent.inner_html
puts location.inner_html
puts result.inner_html

game = {}
game['date'] = date.inner_html
game['opponent'] = opponent.inner_html
game['location'] = location.inner_html
game['result'] = result.inner_html

ScraperWiki.save(['date'], game)
end