# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

doc.xpath("//div").each do |table|#kokode syutokusita data ni kaigyou ga hairanai!!!

name = table.search("//span[@class='pp-place-title']/a/span")[1].text
address= table.search("//span[@class='pp-headline-item pp-headline-address']/span")[1].text
tel= table.search("//span[@class='telephone']/nobr")[1].text
url2= table.search("//span[@class='pp-place-title']/a")[1].get_attribute("href")

    
    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => url2
    }
end

  result
end



urls = (1..1).map {|i| "http://maps.google.co.jp/maps?hl=ja&q=%E5%AE%85%E9%85%8D%E5%BC%81%E5%BD%93&ie=UTF8&authuser=0&sa=N&sll=35.679876,139.779645&sspn=0.010000,0.013469&start=#{i}0"}

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), 'Shift_JIS')
  data = parse_doc(doc)
  # (name, furigana) is not unique indeed
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
end# Blank Ruby

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

doc.xpath("//div").each do |table|#kokode syutokusita data ni kaigyou ga hairanai!!!

name = table.search("//span[@class='pp-place-title']/a/span")[1].text
address= table.search("//span[@class='pp-headline-item pp-headline-address']/span")[1].text
tel= table.search("//span[@class='telephone']/nobr")[1].text
url2= table.search("//span[@class='pp-place-title']/a")[1].get_attribute("href")

    
    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'name'     => name,
      'address' => address,
      'tel'    => tel,
      'url2' => url2
    }
end

  result
end



urls = (1..1).map {|i| "http://maps.google.co.jp/maps?hl=ja&q=%E5%AE%85%E9%85%8D%E5%BC%81%E5%BD%93&ie=UTF8&authuser=0&sa=N&sll=35.679876,139.779645&sspn=0.010000,0.013469&start=#{i}0"}

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), 'Shift_JIS')
  data = parse_doc(doc)
  # (name, furigana) is not unique indeed
  ScraperWiki.save(['name', 'address', 'tel', 'url2'], data)
end