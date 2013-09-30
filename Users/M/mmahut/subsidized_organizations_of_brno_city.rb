# Subsidized organizations of Brno city
require 'nokogiri'
require 'cgi'
require 'uri'
require 'open-uri'

html = ScraperWiki.scrape("http://www.brno.cz/sprava-mesta/urady-a-instituce-v-brne/mestske-organizace-a-spolecnosti/")
puts "Start"

docu = Nokogiri::HTML(html)
#docu.each{  |br| br.replace("\n") }

docu.css('div[id = c924]').each_line do |node|
  node.text
  puts "bla"
end



# Subsidized organizations of Brno city
require 'nokogiri'
require 'cgi'
require 'uri'
require 'open-uri'

html = ScraperWiki.scrape("http://www.brno.cz/sprava-mesta/urady-a-instituce-v-brne/mestske-organizace-a-spolecnosti/")
puts "Start"

docu = Nokogiri::HTML(html)
#docu.each{  |br| br.replace("\n") }

docu.css('div[id = c924]').each_line do |node|
  node.text
  puts "bla"
end



