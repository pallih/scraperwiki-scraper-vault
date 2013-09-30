# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  list = doc.xpath('//*[@id="SearchList"]/li')
  
  # Note tr[1] is actually a table header
  list.each do |li|
    a = li.xpath('div[2]/h4/a')

    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  day = ""
  time = ""
  address = ""
  tel = ""
  fax = ""
  website = ""
  email = ""

  details = doc.xpath('//*[@id="ShopDate"]/table/tr')
  details.each do |detail|
    th = detail.xpath('th').text
    case th
    when 'TEL'
      tel = detail.xpath('td').text
    when '住所'
      address = detail.xpath('td').text
    when 'FAX'
      fax = detail.xpath('td').text
    when 'URL'
      website = detail.xpath('td/a')[0]
      website = website[0].nil? ? "" : website[0]["href"]
    else
      puts 'skip'
    end
  end
  #address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  
  #td3 = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  #td4 = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  #website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  #website = website[0].nil? ? "" : website[0]["href"]
  
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
  url = "http://dl.dropbox.com/u/18379862/nara/nara.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

# http://www.kosodate.pref.nara.jp/search/index.php?act=list&p=s3&v=500&s=1

records = []

urls.each{ |url|
    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
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
  list = doc.xpath('//*[@id="SearchList"]/li')
  
  # Note tr[1] is actually a table header
  list.each do |li|
    a = li.xpath('div[2]/h4/a')

    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  day = ""
  time = ""
  address = ""
  tel = ""
  fax = ""
  website = ""
  email = ""

  details = doc.xpath('//*[@id="ShopDate"]/table/tr')
  details.each do |detail|
    th = detail.xpath('th').text
    case th
    when 'TEL'
      tel = detail.xpath('td').text
    when '住所'
      address = detail.xpath('td').text
    when 'FAX'
      fax = detail.xpath('td').text
    when 'URL'
      website = detail.xpath('td/a')[0]
      website = website[0].nil? ? "" : website[0]["href"]
    else
      puts 'skip'
    end
  end
  #address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  
  #td3 = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  #td4 = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  #website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  #website = website[0].nil? ? "" : website[0]["href"]
  
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
  url = "http://dl.dropbox.com/u/18379862/nara/nara.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

# http://www.kosodate.pref.nara.jp/search/index.php?act=list&p=s3&v=500&s=1

records = []

urls.each{ |url|
    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
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
  list = doc.xpath('//*[@id="SearchList"]/li')
  
  # Note tr[1] is actually a table header
  list.each do |li|
    a = li.xpath('div[2]/h4/a')

    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  day = ""
  time = ""
  address = ""
  tel = ""
  fax = ""
  website = ""
  email = ""

  details = doc.xpath('//*[@id="ShopDate"]/table/tr')
  details.each do |detail|
    th = detail.xpath('th').text
    case th
    when 'TEL'
      tel = detail.xpath('td').text
    when '住所'
      address = detail.xpath('td').text
    when 'FAX'
      fax = detail.xpath('td').text
    when 'URL'
      website = detail.xpath('td/a')[0]
      website = website[0].nil? ? "" : website[0]["href"]
    else
      puts 'skip'
    end
  end
  #address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  
  #td3 = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  #td4 = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  #website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  #website = website[0].nil? ? "" : website[0]["href"]
  
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
  url = "http://dl.dropbox.com/u/18379862/nara/nara.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

# http://www.kosodate.pref.nara.jp/search/index.php?act=list&p=s3&v=500&s=1

records = []

urls.each{ |url|
    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
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
  list = doc.xpath('//*[@id="SearchList"]/li')
  
  # Note tr[1] is actually a table header
  list.each do |li|
    a = li.xpath('div[2]/h4/a')

    next if a.xpath("@href").nil? 
    result << {
      'url' => a.xpath("@href")
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="Main"]/div[2]/h3').text
  day = ""
  time = ""
  address = ""
  tel = ""
  fax = ""
  website = ""
  email = ""

  details = doc.xpath('//*[@id="ShopDate"]/table/tr')
  details.each do |detail|
    th = detail.xpath('th').text
    case th
    when 'TEL'
      tel = detail.xpath('td').text
    when '住所'
      address = detail.xpath('td').text
    when 'FAX'
      fax = detail.xpath('td').text
    when 'URL'
      website = detail.xpath('td/a')[0]
      website = website[0].nil? ? "" : website[0]["href"]
    else
      puts 'skip'
    end
  end
  #address = doc.xpath('//*[@id="ShopDate"]/table/tr[2]/td').text
  
  #td3 = doc.xpath('//*[@id="ShopDate"]/table/tr[3]/td').text
  #td4 = doc.xpath('//*[@id="ShopDate"]/table/tr[4]/td').text
  #website = doc.xpath('//*[@id="ShopDate"]/table/tr[5]/td/a')
  #website = website[0].nil? ? "" : website[0]["href"]
  
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
  url = "http://dl.dropbox.com/u/18379862/nara/nara.html"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'utf-8')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(3)
end

puts "url count is #{urls.length}"

# http://www.kosodate.pref.nara.jp/search/index.php?act=list&p=s3&v=500&s=1

records = []

urls.each{ |url|
    url = "http://www.kosodate.pref.nara.jp/search/#{url['url']}"
    data = Nokogiri::HTML.parse(open(url), nil, 'Shift_JIS')
    records << parse_detail(data)
    ScraperWiki.save(unique_keys=['name'], data=records)
    records = []
    sleep(3)  
}
#puts "#{records}"


