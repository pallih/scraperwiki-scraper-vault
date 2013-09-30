# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/madonna-mw0000268192"

doc = Nokogiri.HTML(open(url))

details = doc.search('.details')
puts details

  album = {}
  album[:id] = "1"
  puts album[:id]
  album[:url] = url
  puts album[:url]
  album[:release_date] = details.search('.release-date').inner_text
  puts album[:release_date]
  album[:duration] = details.search('.duration').inner_text
  puts album[:release_date]
  album[:genres] = details.search('.genres').inner_text
  puts album[:genres]
  album[:styles] = details.search('.styles').inner_text
  puts album[:styles]
  album[:moods] = details.search('.sidebar-module moods').inner_text
  puts album[:moods]
  album[:themes] = details.search('.sidebar-module themes').inner_text
  puts album[:themes]

ScraperWiki.save([:id], album)# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/madonna-mw0000268192"

doc = Nokogiri.HTML(open(url))

details = doc.search('.details')
puts details

  album = {}
  album[:id] = "1"
  puts album[:id]
  album[:url] = url
  puts album[:url]
  album[:release_date] = details.search('.release-date').inner_text
  puts album[:release_date]
  album[:duration] = details.search('.duration').inner_text
  puts album[:release_date]
  album[:genres] = details.search('.genres').inner_text
  puts album[:genres]
  album[:styles] = details.search('.styles').inner_text
  puts album[:styles]
  album[:moods] = details.search('.sidebar-module moods').inner_text
  puts album[:moods]
  album[:themes] = details.search('.sidebar-module themes').inner_text
  puts album[:themes]

ScraperWiki.save([:id], album)