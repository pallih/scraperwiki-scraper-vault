# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  list = doc.xpath('//*[@id="tmp_contents"]/div[2]/table/tr[1]/th/p/a')
  puts list

  # Note tr[1] is actually a table header
  list.each do |t|
    a = t.xpath('tr[1]/th/p/a')
    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  day = ""
  time = ""

  tel = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  fax = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = ""

  services = doc.xpath('//*[@id="ServiceDetail"]/p').text
  feeding = "○" unless services.index("授乳室").nil? 
  diaper = "○" unless services.index("おむつ替え").nil? 
  hotwater = "○" unless services.index("ミルクのお湯提供").nil? 
  return nil if feeding.nil? && diaper.nil? && hotwater.nil? 
 
  puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
  {
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

urls = []
for i in 0..0 do
  url = "http://dl.dropboxusercontent.com/u/18379862/chiba/index.html"
  listPage = open(url)
  puts listPage
  doc = Nokogiri::HTML.parse(listPage, nil, 'utf-8')
  puts doc
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

puts urls

records = []

#urls.each{ |url|
#    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
#    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
#    records << parse_detail(data)
#    ScraperWiki.save(unique_keys=['name'], data=records)
#    records = []
#    sleep(3)  
#}
#puts "#{records}"


# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  list = doc.xpath('//*[@id="tmp_contents"]/div[2]/table/tr[1]/th/p/a')
  puts list

  # Note tr[1] is actually a table header
  list.each do |t|
    a = t.xpath('tr[1]/th/p/a')
    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  day = ""
  time = ""

  tel = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  fax = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = ""

  services = doc.xpath('//*[@id="ServiceDetail"]/p').text
  feeding = "○" unless services.index("授乳室").nil? 
  diaper = "○" unless services.index("おむつ替え").nil? 
  hotwater = "○" unless services.index("ミルクのお湯提供").nil? 
  return nil if feeding.nil? && diaper.nil? && hotwater.nil? 
 
  puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
  {
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

urls = []
for i in 0..0 do
  url = "http://dl.dropboxusercontent.com/u/18379862/chiba/index.html"
  listPage = open(url)
  puts listPage
  doc = Nokogiri::HTML.parse(listPage, nil, 'utf-8')
  puts doc
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

puts urls

records = []

#urls.each{ |url|
#    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
#    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
#    records << parse_detail(data)
#    ScraperWiki.save(unique_keys=['name'], data=records)
#    records = []
#    sleep(3)  
#}
#puts "#{records}"


# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  list = doc.xpath('//*[@id="tmp_contents"]/div[2]/table/tr[1]/th/p/a')
  puts list

  # Note tr[1] is actually a table header
  list.each do |t|
    a = t.xpath('tr[1]/th/p/a')
    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  day = ""
  time = ""

  tel = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  fax = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = ""

  services = doc.xpath('//*[@id="ServiceDetail"]/p').text
  feeding = "○" unless services.index("授乳室").nil? 
  diaper = "○" unless services.index("おむつ替え").nil? 
  hotwater = "○" unless services.index("ミルクのお湯提供").nil? 
  return nil if feeding.nil? && diaper.nil? && hotwater.nil? 
 
  puts "#{name}/#{address}/#{tel}/#{fax}/#{website}/#{email}/#{feeding}/#{diaper}/#{hotwater}/#{time}"
  {
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

urls = []
for i in 0..0 do
  url = "http://dl.dropboxusercontent.com/u/18379862/chiba/index.html"
  listPage = open(url)
  puts listPage
  doc = Nokogiri::HTML.parse(listPage, nil, 'utf-8')
  puts doc
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

puts urls

records = []

#urls.each{ |url|
#    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
#    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
#    records << parse_detail(data)
#    ScraperWiki.save(unique_keys=['name'], data=records)
#    records = []
#    sleep(3)  
#}
#puts "#{records}"


