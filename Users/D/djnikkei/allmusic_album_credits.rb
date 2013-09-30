# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/madonna-mw0000268192/credits"

doc = Nokogiri.HTML(open(url))

rows = doc.search('tr')

rows.each do |row|
  link = row.search('a')[0]

  credit = {}
  
  credit[:url] = url
  puts url[:url]
  credit[:name] = link.inner_text
  puts credit[:name]
  credit[:url] = link[:href]
  puts credit[:url]
  credit[:role] = row.search('.name-credit').inner_text
  puts credit[:role]

ScraperWiki.save([:name], credit)
end# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/madonna-mw0000268192/credits"

doc = Nokogiri.HTML(open(url))

rows = doc.search('tr')

rows.each do |row|
  link = row.search('a')[0]

  credit = {}
  
  credit[:url] = url
  puts url[:url]
  credit[:name] = link.inner_text
  puts credit[:name]
  credit[:url] = link[:href]
  puts credit[:url]
  credit[:role] = row.search('.name-credit').inner_text
  puts credit[:role]

ScraperWiki.save([:name], credit)
end