# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/ok-computer-mw0000024289"

doc = Nokogiri.XML(open(url))

details = doc.search('.details')
genres = details.search('.genres')
styles = details.search('.styles')
moods = doc.search("//div[@class='sidebar-module moods']")
element1 = moods.at('h4')
element1.content = ""
themes = doc.search("//div[@class='sidebar-module themes']")
element2 = themes.at('h4')
element2.content = ""
puts details
puts moods

  album = {}
  album[:id] = "1"
  puts album[:id]
  album[:artist] = doc.search('.album-artist').inner_text
  puts album[:artist]
  album[:title] = doc.search('.album-title').inner_text.lstrip.rstrip
  puts album[:title]
  album[:url] = url
  puts album[:url]
  album[:release_date] = doc.search('.release-date').inner_text
  puts album[:release_date]
  album[:duration] = doc.search('.duration').inner_text.lstrip.rstrip
  puts album[:duration]

  album[:genres] = genres.search('li').map{|p| p.text}.join(", ")
  puts album[:genres]

  album[:styles] = styles.search('li').map{|p| p.text}.join(", ")
  puts album[:styles]

  album[:moods] = moods.search('li').map{|p| p.text}.join(", ")
  puts album[:moods]

  album[:themes] = themes.search('li').map{|p| p.text}.join(", ")
  puts album[:themes]

ScraperWiki.save([:id], album)# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'

url = "http://www.allmusic.com/album/ok-computer-mw0000024289"

doc = Nokogiri.XML(open(url))

details = doc.search('.details')
genres = details.search('.genres')
styles = details.search('.styles')
moods = doc.search("//div[@class='sidebar-module moods']")
element1 = moods.at('h4')
element1.content = ""
themes = doc.search("//div[@class='sidebar-module themes']")
element2 = themes.at('h4')
element2.content = ""
puts details
puts moods

  album = {}
  album[:id] = "1"
  puts album[:id]
  album[:artist] = doc.search('.album-artist').inner_text
  puts album[:artist]
  album[:title] = doc.search('.album-title').inner_text.lstrip.rstrip
  puts album[:title]
  album[:url] = url
  puts album[:url]
  album[:release_date] = doc.search('.release-date').inner_text
  puts album[:release_date]
  album[:duration] = doc.search('.duration').inner_text.lstrip.rstrip
  puts album[:duration]

  album[:genres] = genres.search('li').map{|p| p.text}.join(", ")
  puts album[:genres]

  album[:styles] = styles.search('li').map{|p| p.text}.join(", ")
  puts album[:styles]

  album[:moods] = moods.search('li').map{|p| p.text}.join(", ")
  puts album[:moods]

  album[:themes] = themes.search('li').map{|p| p.text}.join(", ")
  puts album[:themes]

ScraperWiki.save([:id], album)