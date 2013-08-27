# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_detail(doc)
#div[2]/table[1]/tbody/tr/td[1]/table/tbody
  table = doc.xpath('//body/div[2]/table[1]/tr/td[1]/table')
  services = table.xpath('./tr[4]/td[2]/font/strong').text
  return nil unless services.index("要優待券").nil? 

  feeding = services.index("授乳").nil? ? "" :"○"
  diaper = (services.index("オムツ替え").nil? and services.index("おむつ替え").nil?) ? "" :"○"
  hotwater = services.index("粉ミルク用のお湯提供").nil? ? "" : "○"

  return nil if feeding == "" and diaper == "" and hotwater == "" 

  name =table.xpath('./tr[2]/td[2]/font').text
  address = table.xpath('./tr[6]/td[2]/font').text

  telnode = table.xpath('./td[2]/font')
  tel = table.xpath('./td[2]/font').text
  day = table.xpath('./tr[9]/td[2]/font').text
  time = table.xpath('./tr[11]/td[2]/font').text
  website = table.xpath('./td[4]/font/a').text
  email = table.xpath('./tr[14]/td[2]/font/a').text
  puts "#{name}/#{address}/#{tel}/#{day}/#{time}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}"

  {
    "name" =>name ,
    "address" => address,
    "tel" => tel,
    "day" => day,
    "time" => time,
    "website" => website,
    "email" => email,
    "feeding" => feeding,
    "diaper" => diaper,
    "hotwater" => hotwater,
    "memo" => services
  }
end

records = []
for i in 1..568 do
  begin
    url = "http://web2.pref.kochi.jp/~kosodateouen/detail.asp?recno=#{i}"
    #puts "Fetching #{url}"
    page = Nokogiri::HTML.parse(open(url))
    result = parse_detail(page)
    records << result unless result.nil? 
  rescue
  end
  sleep(30)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_detail(doc)
#div[2]/table[1]/tbody/tr/td[1]/table/tbody
  table = doc.xpath('//body/div[2]/table[1]/tr/td[1]/table')
  services = table.xpath('./tr[4]/td[2]/font/strong').text
  return nil unless services.index("要優待券").nil? 

  feeding = services.index("授乳").nil? ? "" :"○"
  diaper = (services.index("オムツ替え").nil? and services.index("おむつ替え").nil?) ? "" :"○"
  hotwater = services.index("粉ミルク用のお湯提供").nil? ? "" : "○"

  return nil if feeding == "" and diaper == "" and hotwater == "" 

  name =table.xpath('./tr[2]/td[2]/font').text
  address = table.xpath('./tr[6]/td[2]/font').text

  telnode = table.xpath('./td[2]/font')
  tel = table.xpath('./td[2]/font').text
  day = table.xpath('./tr[9]/td[2]/font').text
  time = table.xpath('./tr[11]/td[2]/font').text
  website = table.xpath('./td[4]/font/a').text
  email = table.xpath('./tr[14]/td[2]/font/a').text
  puts "#{name}/#{address}/#{tel}/#{day}/#{time}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}"

  {
    "name" =>name ,
    "address" => address,
    "tel" => tel,
    "day" => day,
    "time" => time,
    "website" => website,
    "email" => email,
    "feeding" => feeding,
    "diaper" => diaper,
    "hotwater" => hotwater,
    "memo" => services
  }
end

records = []
for i in 1..568 do
  begin
    url = "http://web2.pref.kochi.jp/~kosodateouen/detail.asp?recno=#{i}"
    #puts "Fetching #{url}"
    page = Nokogiri::HTML.parse(open(url))
    result = parse_detail(page)
    records << result unless result.nil? 
  rescue
  end
  sleep(30)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_detail(doc)
#div[2]/table[1]/tbody/tr/td[1]/table/tbody
  table = doc.xpath('//body/div[2]/table[1]/tr/td[1]/table')
  services = table.xpath('./tr[4]/td[2]/font/strong').text
  return nil unless services.index("要優待券").nil? 

  feeding = services.index("授乳").nil? ? "" :"○"
  diaper = (services.index("オムツ替え").nil? and services.index("おむつ替え").nil?) ? "" :"○"
  hotwater = services.index("粉ミルク用のお湯提供").nil? ? "" : "○"

  return nil if feeding == "" and diaper == "" and hotwater == "" 

  name =table.xpath('./tr[2]/td[2]/font').text
  address = table.xpath('./tr[6]/td[2]/font').text

  telnode = table.xpath('./td[2]/font')
  tel = table.xpath('./td[2]/font').text
  day = table.xpath('./tr[9]/td[2]/font').text
  time = table.xpath('./tr[11]/td[2]/font').text
  website = table.xpath('./td[4]/font/a').text
  email = table.xpath('./tr[14]/td[2]/font/a').text
  puts "#{name}/#{address}/#{tel}/#{day}/#{time}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}"

  {
    "name" =>name ,
    "address" => address,
    "tel" => tel,
    "day" => day,
    "time" => time,
    "website" => website,
    "email" => email,
    "feeding" => feeding,
    "diaper" => diaper,
    "hotwater" => hotwater,
    "memo" => services
  }
end

records = []
for i in 1..568 do
  begin
    url = "http://web2.pref.kochi.jp/~kosodateouen/detail.asp?recno=#{i}"
    #puts "Fetching #{url}"
    page = Nokogiri::HTML.parse(open(url))
    result = parse_detail(page)
    records << result unless result.nil? 
  rescue
  end
  sleep(30)
end

puts records.length
ScraperWiki.save(unique_keys=['name'], data=records)

