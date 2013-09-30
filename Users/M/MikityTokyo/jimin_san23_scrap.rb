# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

doc = Nokogiri::HTML(open("http://dl.dropboxusercontent.com/u/433935/jimin.html"))

#puts doc.xpath('//table[@class = "sp-table"]/tr/td[@class = "sen-hp"]/ul/li/a[contains(@href, "twitter")]').text

doc.xpath('//table[@class = "sp-table"]/tr').each do |node|
    data = {
      "area" => node.xpath('td[@class = "sen-area"]').text,
      "name" => node.xpath('td[@class = "sen-nm"]').text,
      "twitter" => node.xpath('td[@class = "sen-hp"]/ul/li/a[contains(@href, "twitter")]'),
      "careers" => node.xpath('td[@class = "sen-kei"]').text
  }
  ScraperWiki::save_sqlite(['name'], data) 
end


# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

doc = Nokogiri::HTML(open("http://dl.dropboxusercontent.com/u/433935/jimin.html"))

#puts doc.xpath('//table[@class = "sp-table"]/tr/td[@class = "sen-hp"]/ul/li/a[contains(@href, "twitter")]').text

doc.xpath('//table[@class = "sp-table"]/tr').each do |node|
    data = {
      "area" => node.xpath('td[@class = "sen-area"]').text,
      "name" => node.xpath('td[@class = "sen-nm"]').text,
      "twitter" => node.xpath('td[@class = "sen-hp"]/ul/li/a[contains(@href, "twitter")]'),
      "careers" => node.xpath('td[@class = "sen-kei"]').text
  }
  ScraperWiki::save_sqlite(['name'], data) 
end


