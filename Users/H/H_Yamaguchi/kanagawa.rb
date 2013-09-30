# -*- coding: utf-8 -*-

# POSTしか受け付けないようなので、取得NG

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end


def parse_detail(doc)

  details = doc.xpath('//*[@id="contentKpass"]/div/div/table/tr')
  
  records = []

  details.each do |detail|
    day = ""
    time = ""
    tel = ""
    fax = ""
    website = ""
    email = ""

    name = detail.xpath('td[1]/a').text
    address = detail.xpath('td[2]').text
    services = detail.xpath('td[4]/img')
    #feeding = 
    #feeding = services.xpath('*[@src="/kpass/img/ico_service01-01.gif"]')
    #puts feeding
    #puts services.index('img[@src="/kpass/img/ico_service01-01.gif"]')
    #feeding = "○" unless detail.index('td[4]/img[@src="/kpass/img/ico_service01-01.gif"]').nil?
    feeding = "○" if detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').length > 0
    diaper = "○" if detail.xpath("td[4]/img[@alt='おむつ替えスペース']").length > 0
    hotwater = "○" if detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").length > 0

    #feeding = "○" unless detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').nil? 
    #diaper = "○" unless detail.xpath("td[4]/img[@alt='おむつ替えスペース']").nil? 
    #hotwater = "○" unless detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").nil? 
    puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
    records << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel,
      "fax" => fax,
      "email" => email,
      "website" => website,
      "time" => time,
      "day" => day
    }
  end
  records = records.select do |item|
   !(item["feeding"].nil? && item["diaper"].nil? && item["hotwater"].nil?)
  end
  puts records
  records = records.select do |item|
    !item["name"].empty? 
  end
  records
end

records = []

for i in 1..90 do
  url = "http://c.rakuraku.or.jp/k-pass/search/list/page/#{i}"
  data = Nokogiri::HTML.parse(open(url))
  records += parse_detail(data)
  sleep(3)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

# POSTしか受け付けないようなので、取得NG

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end


def parse_detail(doc)

  details = doc.xpath('//*[@id="contentKpass"]/div/div/table/tr')
  
  records = []

  details.each do |detail|
    day = ""
    time = ""
    tel = ""
    fax = ""
    website = ""
    email = ""

    name = detail.xpath('td[1]/a').text
    address = detail.xpath('td[2]').text
    services = detail.xpath('td[4]/img')
    #feeding = 
    #feeding = services.xpath('*[@src="/kpass/img/ico_service01-01.gif"]')
    #puts feeding
    #puts services.index('img[@src="/kpass/img/ico_service01-01.gif"]')
    #feeding = "○" unless detail.index('td[4]/img[@src="/kpass/img/ico_service01-01.gif"]').nil?
    feeding = "○" if detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').length > 0
    diaper = "○" if detail.xpath("td[4]/img[@alt='おむつ替えスペース']").length > 0
    hotwater = "○" if detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").length > 0

    #feeding = "○" unless detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').nil? 
    #diaper = "○" unless detail.xpath("td[4]/img[@alt='おむつ替えスペース']").nil? 
    #hotwater = "○" unless detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").nil? 
    puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
    records << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel,
      "fax" => fax,
      "email" => email,
      "website" => website,
      "time" => time,
      "day" => day
    }
  end
  records = records.select do |item|
   !(item["feeding"].nil? && item["diaper"].nil? && item["hotwater"].nil?)
  end
  puts records
  records = records.select do |item|
    !item["name"].empty? 
  end
  records
end

records = []

for i in 1..90 do
  url = "http://c.rakuraku.or.jp/k-pass/search/list/page/#{i}"
  data = Nokogiri::HTML.parse(open(url))
  records += parse_detail(data)
  sleep(3)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

# POSTしか受け付けないようなので、取得NG

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end


def parse_detail(doc)

  details = doc.xpath('//*[@id="contentKpass"]/div/div/table/tr')
  
  records = []

  details.each do |detail|
    day = ""
    time = ""
    tel = ""
    fax = ""
    website = ""
    email = ""

    name = detail.xpath('td[1]/a').text
    address = detail.xpath('td[2]').text
    services = detail.xpath('td[4]/img')
    #feeding = 
    #feeding = services.xpath('*[@src="/kpass/img/ico_service01-01.gif"]')
    #puts feeding
    #puts services.index('img[@src="/kpass/img/ico_service01-01.gif"]')
    #feeding = "○" unless detail.index('td[4]/img[@src="/kpass/img/ico_service01-01.gif"]').nil?
    feeding = "○" if detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').length > 0
    diaper = "○" if detail.xpath("td[4]/img[@alt='おむつ替えスペース']").length > 0
    hotwater = "○" if detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").length > 0

    #feeding = "○" unless detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').nil? 
    #diaper = "○" unless detail.xpath("td[4]/img[@alt='おむつ替えスペース']").nil? 
    #hotwater = "○" unless detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").nil? 
    puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
    records << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel,
      "fax" => fax,
      "email" => email,
      "website" => website,
      "time" => time,
      "day" => day
    }
  end
  records = records.select do |item|
   !(item["feeding"].nil? && item["diaper"].nil? && item["hotwater"].nil?)
  end
  puts records
  records = records.select do |item|
    !item["name"].empty? 
  end
  records
end

records = []

for i in 1..90 do
  url = "http://c.rakuraku.or.jp/k-pass/search/list/page/#{i}"
  data = Nokogiri::HTML.parse(open(url))
  records += parse_detail(data)
  sleep(3)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

# POSTしか受け付けないようなので、取得NG

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end


def parse_detail(doc)

  details = doc.xpath('//*[@id="contentKpass"]/div/div/table/tr')
  
  records = []

  details.each do |detail|
    day = ""
    time = ""
    tel = ""
    fax = ""
    website = ""
    email = ""

    name = detail.xpath('td[1]/a').text
    address = detail.xpath('td[2]').text
    services = detail.xpath('td[4]/img')
    #feeding = 
    #feeding = services.xpath('*[@src="/kpass/img/ico_service01-01.gif"]')
    #puts feeding
    #puts services.index('img[@src="/kpass/img/ico_service01-01.gif"]')
    #feeding = "○" unless detail.index('td[4]/img[@src="/kpass/img/ico_service01-01.gif"]').nil?
    feeding = "○" if detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').length > 0
    diaper = "○" if detail.xpath("td[4]/img[@alt='おむつ替えスペース']").length > 0
    hotwater = "○" if detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").length > 0

    #feeding = "○" unless detail.xpath('td[4]/img[@alt="授乳・調乳スペース"]').nil? 
    #diaper = "○" unless detail.xpath("td[4]/img[@alt='おむつ替えスペース']").nil? 
    #hotwater = "○" unless detail.xpath("td[4]/img[@alt='粉ミルク用のお湯の提供']").nil? 
    puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
    records << {
      "name" =>name ,
      "diaper" => diaper,
      "feeding" => feeding,
      "hotwater" => hotwater,
      "address" => address,
      "tel" => tel,
      "fax" => fax,
      "email" => email,
      "website" => website,
      "time" => time,
      "day" => day
    }
  end
  records = records.select do |item|
   !(item["feeding"].nil? && item["diaper"].nil? && item["hotwater"].nil?)
  end
  puts records
  records = records.select do |item|
    !item["name"].empty? 
  end
  records
end

records = []

for i in 1..90 do
  url = "http://c.rakuraku.or.jp/k-pass/search/list/page/#{i}"
  data = Nokogiri::HTML.parse(open(url))
  records += parse_detail(data)
  sleep(3)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

