# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

data = {}

doc = Nokogiri::HTML(open("http://j-ishin.jp/candidate2013/"))


doc.xpath('//div[@class = "info"]').each do |div|

  data = {
    "area" => div.xpath('p[@class = "area"]').text,
    "name" => div.xpath('p[@class = "name-kanji"]').text,
    "name-kana" => div.xpath('p[@class = "name-kana"]').text,
    "sns-btns" => div.xpath('ul[@class = "sns-btns"]/li/a[contains(@href, "twitter")]'),
    "careers" => div.xpath('ul[@class = "careers"]').text
 }

ScraperWiki::save_sqlite(['name'], data) 
end



