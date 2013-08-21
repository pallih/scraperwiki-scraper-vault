# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_main(doc)
  result = []

  doc.xpath('//table[@id="black"]//tr').each do |tr|
    diaper = ""
    feeding =""
    water = ""
    tr.xpath('./td[4]//li').each do |li|
      puts li
      if li.inner_text.include?("授乳")
        feeding = "○"
      end 

      if li.inner_text.include?("ミルク用お湯")
        water = "○"
      end 

      if li.inner_text.include?("オムツ替え")
        diaper = "○"
      end

    end
    result << {
      "name" => tr.xpath('./td[1]').inner_text.strip,
      "tel" =>  tr.xpath('./td[2]').inner_text.strip,
      "address" => tr.xpath('./td[3]').inner_text.strip,
      "diaper" => diaper,
      "feeding" => feeding,
      "water" => water,
      "memo" => tr.xpath('./td[5]').inner_text.strip
    }
  end

  result
end

url = "http://www.city.yukuhashi.fukuoka.jp/kakuka/kodomo/babyshisetsu.html"
puts "Fetching #{url}"

mainPage = Nokogiri::HTML(open(url))
puts mainPage

records =  parse_main(mainPage)

puts records

ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_main(doc)
  result = []

  doc.xpath('//table[@id="black"]//tr').each do |tr|
    diaper = ""
    feeding =""
    water = ""
    tr.xpath('./td[4]//li').each do |li|
      puts li
      if li.inner_text.include?("授乳")
        feeding = "○"
      end 

      if li.inner_text.include?("ミルク用お湯")
        water = "○"
      end 

      if li.inner_text.include?("オムツ替え")
        diaper = "○"
      end

    end
    result << {
      "name" => tr.xpath('./td[1]').inner_text.strip,
      "tel" =>  tr.xpath('./td[2]').inner_text.strip,
      "address" => tr.xpath('./td[3]').inner_text.strip,
      "diaper" => diaper,
      "feeding" => feeding,
      "water" => water,
      "memo" => tr.xpath('./td[5]').inner_text.strip
    }
  end

  result
end

url = "http://www.city.yukuhashi.fukuoka.jp/kakuka/kodomo/babyshisetsu.html"
puts "Fetching #{url}"

mainPage = Nokogiri::HTML(open(url))
puts mainPage

records =  parse_main(mainPage)

puts records

ScraperWiki.save(unique_keys=['name'], data=records)

