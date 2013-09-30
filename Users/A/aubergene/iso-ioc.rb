require 'open-uri'
require 'nokogiri'

doc = Nokogiri.HTML(open("http://www.statoids.com/wab.html").read)

rows = []

doc.css('tr')[1..-2].each do |row|
  cells = row.css('td')
  iso = cells[1].text.sub(/[[:space:]]/,'')
  ioc = cells[6].text.sub(/[[:space:]]/,'')
  rows << {ioc => iso}
  ScraperWiki::save_sqlite(['country'], data)  
end

require 'open-uri'
require 'nokogiri'

doc = Nokogiri.HTML(open("http://www.statoids.com/wab.html").read)

rows = []

doc.css('tr')[1..-2].each do |row|
  cells = row.css('td')
  iso = cells[1].text.sub(/[[:space:]]/,'')
  ioc = cells[6].text.sub(/[[:space:]]/,'')
  rows << {ioc => iso}
  ScraperWiki::save_sqlite(['country'], data)  
end

