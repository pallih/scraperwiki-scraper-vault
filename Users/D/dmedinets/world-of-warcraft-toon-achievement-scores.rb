# World of Warcraft - scrape the achievement score of guild members.

require 'json'
require 'nokogiri'
#require 'rubygems'
#require 'hpricot'
#require 'date'
#require 'net/https'
#require 'json'
require 'open-uri'

toons = JSON.parse(open("http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=veritas-roster").read)

class Toon
  def initialize(_name, _url, _score)
    @name = _name
    @url = _url
    @score = _score
  end
  def name
    @name
  end
  def url
    @url
  end
  def score
    @score
  end
end

data = []

toons.each do |toon|
  toon_url = "http://us.battle.net#{toon['url']}achievement"
  html = ScraperWiki.scrape(toon_url)
  next if html.nil? 
  doc = Nokogiri::HTML(html)
  next if doc.nil? 
  toon_achievement_score_node = doc.css(".achievement-points").first
  next if toon_achievement_score_node.nil? 
  toon_achievement_score = toon_achievement_score_node.text.strip  
  data << Toon.new(toon['name'], toon_url, toon_achievement_score)
end

sorted_data = data.sort! do |a, b|
   puts "#{a.name}[#{a.score}] -- #{b.name}[#{b.score}]"
   a.score.to_i <=> b.score.to_i
end


sorted_data[0..25].each_with_index do |toon, index|
  puts "#{index}: #{toon.name}"
  ScraperWiki.save(unique_keys = ['name'],  data = { 'name' => toon.name, 'url' => toon.url,  'achievement_score' => toon.score })
end


