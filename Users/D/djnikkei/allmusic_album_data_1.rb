# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/artist/madonna-mn0000237205"

doc = Nokogiri.HTML(open(url))

rows = doc.search('tr')
puts rows

rows.each do |row|
link = row.search('a')[0]
#puts link

album = {}
album[:name] = row.search('a.title.full-title').inner_text
puts album[:name]
album[:url] = link[:href]
#puts album[:url]
album[:artist_URL] = url
#puts album[:artist_URL]
album[:year] = row.search('.year').inner_text
#puts album[:year]
album[:label] = row.search('.label').inner_text
#puts album[:label]

ScraperWiki.save([:url], album)
end