# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  anchors = doc.xpath('//*[@id="ouennomise"]/div[3]/div/div[3]/div[1]/h3/a')
  
  # Note tr[1] is actually a table header
  anchors.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    next unless a["href"].include?("detail")
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[1]/h3').text
  address = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td/text()[2]').text
  day = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td').text
  time = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[2]/td').text

  tel = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[4]/td').text
  fax = ""
  website = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[6]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[7]/td/a')
  email = email[0].nil? ? "" : email[0]["href"]

  services = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[2]/div[2]/dl/dl/dd[@class="honobono"]').text
  feeding = ""
  diaper = ""
  hotwater = ""
  feeding = "○" unless services.index("授乳スペース").nil? 
  diaper = "○" unless services.index("おむつ替えコーナー").nil? 
  hotwater = "○" unless services.index("ミルク用のお湯の提供").nil? 
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
  url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/list.cgi?page_offset=#{i*20}&shichoson=11/13/14/15/16/17/18/19/22/23/24/25/29/30/36/37/32/33/34/39/40/41/42/43/44/45/46/47/48/35/49/50/51&honobono=1/2/3"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end


#records = []
puts "url count is #{urls.length}"

#ScraperWiki.save(unique_keys=['url'], data=urls)

#urls = []

records = []

urls.each{ |url|
    url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    ScraperWiki.save(unique_keys=['name'], data=records)
    records = []
    sleep(3)  
}
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
  anchors = doc.xpath('//*[@id="ouennomise"]/div[3]/div/div[3]/div[1]/h3/a')
  
  # Note tr[1] is actually a table header
  anchors.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    next unless a["href"].include?("detail")
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[1]/h3').text
  address = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td/text()[2]').text
  day = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td').text
  time = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[2]/td').text

  tel = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[4]/td').text
  fax = ""
  website = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[6]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[7]/td/a')
  email = email[0].nil? ? "" : email[0]["href"]

  services = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[2]/div[2]/dl/dl/dd[@class="honobono"]').text
  feeding = ""
  diaper = ""
  hotwater = ""
  feeding = "○" unless services.index("授乳スペース").nil? 
  diaper = "○" unless services.index("おむつ替えコーナー").nil? 
  hotwater = "○" unless services.index("ミルク用のお湯の提供").nil? 
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
  url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/list.cgi?page_offset=#{i*20}&shichoson=11/13/14/15/16/17/18/19/22/23/24/25/29/30/36/37/32/33/34/39/40/41/42/43/44/45/46/47/48/35/49/50/51&honobono=1/2/3"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end


#records = []
puts "url count is #{urls.length}"

#ScraperWiki.save(unique_keys=['url'], data=urls)

#urls = []

records = []

urls.each{ |url|
    url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    ScraperWiki.save(unique_keys=['name'], data=records)
    records = []
    sleep(3)  
}
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
  anchors = doc.xpath('//*[@id="ouennomise"]/div[3]/div/div[3]/div[1]/h3/a')
  
  # Note tr[1] is actually a table header
  anchors.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    next unless a["href"].include?("detail")
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[1]/h3').text
  address = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td/text()[2]').text
  day = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td').text
  time = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[2]/td').text

  tel = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[4]/td').text
  fax = ""
  website = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[6]/td/a')
  website = website[0].nil? ? "" : website[0]["href"]
  email = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[1]/div/table/tr[7]/td/a')
  email = email[0].nil? ? "" : email[0]["href"]

  services = doc.xpath('//*[@id="ouennomise"]/div[2]/div[1]/div[3]/div[2]/div[2]/dl/dl/dd[@class="honobono"]').text
  feeding = ""
  diaper = ""
  hotwater = ""
  feeding = "○" unless services.index("授乳スペース").nil? 
  diaper = "○" unless services.index("おむつ替えコーナー").nil? 
  hotwater = "○" unless services.index("ミルク用のお湯の提供").nil? 
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
  url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/list.cgi?page_offset=#{i*20}&shichoson=11/13/14/15/16/17/18/19/22/23/24/25/29/30/36/37/32/33/34/39/40/41/42/43/44/45/46/47/48/35/49/50/51&honobono=1/2/3"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end


#records = []
puts "url count is #{urls.length}"

#ScraperWiki.save(unique_keys=['url'], data=urls)

#urls = []

records = []

urls.each{ |url|
    url = "http://www5.pref.iwate.jp/~hp0359/ouennomise/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    ScraperWiki.save(unique_keys=['name'], data=records)
    records = []
    sleep(3)  
}
#puts "#{records}"


