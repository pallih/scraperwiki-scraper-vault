# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

data = {}

doc = Nokogiri::HTML(open("http://www.komei.or.jp/campaign/sanin2013/koho/"))

puts doc.xpath('//a[@class = "snsButtons gotw"]')


doc.xpath('//a[@class = "snsButtons gotw"]').each do |a|

  data = {
#    "area" => div.xpath('p[@class = "area"]').text,
#    "name" => div.xpath('p[@class = "name-kanji"]').text,
#    "name-kana" => div.xpath('p[@class = "name-kana"]').text,
    "twitter" => a.xpath('//a[@class = "snsButtons gotw"]')
#    "careers" => div.xpath('ul[@class = "careers"]').text
 }

ScraperWiki::save_sqlite(['twitter'], data) 
end



# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

data = {}

doc = Nokogiri::HTML(open("http://www.komei.or.jp/campaign/sanin2013/koho/"))

puts doc.xpath('//a[@class = "snsButtons gotw"]')


doc.xpath('//a[@class = "snsButtons gotw"]').each do |a|

  data = {
#    "area" => div.xpath('p[@class = "area"]').text,
#    "name" => div.xpath('p[@class = "name-kanji"]').text,
#    "name-kana" => div.xpath('p[@class = "name-kana"]').text,
    "twitter" => a.xpath('//a[@class = "snsButtons gotw"]')
#    "careers" => div.xpath('ul[@class = "careers"]').text
 }

ScraperWiki::save_sqlite(['twitter'], data) 
end



