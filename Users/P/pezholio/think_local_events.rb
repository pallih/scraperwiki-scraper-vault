require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

url = 'http://www.thinklocal4business.co.uk/CC-EVENTS/'

doc = Nokogiri.HTML(open(url))

puts doc.errors

events = doc.search('.community-events-results-item')

events.each do |event|
  
  puts "Yo!"
  name = event.search('.eventName')[0].inner_text
  puts name

end
require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

url = 'http://www.thinklocal4business.co.uk/CC-EVENTS/'

doc = Nokogiri.HTML(open(url))

puts doc.errors

events = doc.search('.community-events-results-item')

events.each do |event|
  
  puts "Yo!"
  name = event.search('.eventName')[0].inner_text
  puts name

end
