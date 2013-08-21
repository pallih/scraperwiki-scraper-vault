# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_detail(doc)
  result = []
  rows = doc.xpath('//body/table/tr/td')
  #puts rows
  #puts "rows:#{rows}"
  rows.each do |row|
    name =row.xpath('table/tr/td/font/a').text
    services = row.xpath('font[3]').text
    feeding = "○" unless services.index("授乳").nil? 
    diaper = "○" unless (services.index("おむつ").nil? && services.index("オムツ").nil? )
    hotwater = "○" unless services.index("お湯").nil? 
    address = row.xpath('font[4]').text
    tel = row.xpath('font[5]').text.delete("tel. ")
    puts "#{name}/#{address}/#{tel}/#{feeding}/#{diaper}/#{hotwater}"
    result << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel
    }
  end
  result
end

urls = []
records = []

for i in 0..0 do
  url = "http://dl.dropbox.com/u/18379862/shiga/kosodate.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  records = parse_detail(doc)
  ScraperWiki.save(unique_keys=['name'], data=records)
end



# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_detail(doc)
  result = []
  rows = doc.xpath('//body/table/tr/td')
  #puts rows
  #puts "rows:#{rows}"
  rows.each do |row|
    name =row.xpath('table/tr/td/font/a').text
    services = row.xpath('font[3]').text
    feeding = "○" unless services.index("授乳").nil? 
    diaper = "○" unless (services.index("おむつ").nil? && services.index("オムツ").nil? )
    hotwater = "○" unless services.index("お湯").nil? 
    address = row.xpath('font[4]').text
    tel = row.xpath('font[5]').text.delete("tel. ")
    puts "#{name}/#{address}/#{tel}/#{feeding}/#{diaper}/#{hotwater}"
    result << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel
    }
  end
  result
end

urls = []
records = []

for i in 0..0 do
  url = "http://dl.dropbox.com/u/18379862/shiga/kosodate.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  records = parse_detail(doc)
  ScraperWiki.save(unique_keys=['name'], data=records)
end



