# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list(doc)
  result = []

  resultArea = doc.xpath('//div[@class="Shoplist"]')
  resultArea.each do |area|
    a = area.xpath('./h3//a/@href')
    next if a.text.include?("#")
    next if !a.text.include?("shop")
    
    service = area.xpath('./ul/*').inner_text.strip
    puts service
    feeding = service.include? ("授乳")
    diaper = service.include? ("おむつ替え")
    hotwater = service.include? ("ミルクのお湯")

    next if !(feeding or diaper or hotwater) 
    result << {
      'url' => a.text,
      'feeding' => feeding,
      'diaper' => diaper,
      'hotwater' => hotwater
    }
  end

  result
end

def parse_detail(doc, services)
  #//*[@id="FakeTable"]/div[1]/p
  #//*[@id="DShopName"]/div/h2
  name =doc.xpath('//*[@id="DShopName"]/div/h2').text
  address = doc.xpath('//*[@id="FakeTable"]/div[1]/p').text
  tel = doc.xpath('//*[@id="FakeTable"]/div[2]/p').text
  website = doc.xpath('//*[@id="FakeTable"]/div[3]/p/a').text
  time = doc.xpath('//*[@id="FakeTable"]/div[4]/p').text
  day = doc.xpath('//*[@id="FakeTable"]/div[5]/p').text
  day = "利用不可日:#{day}"

  puts "#{name}/#{address}/#{tel}/#{website}/#{time}/#{day}"
  {
    "name" =>name ,
    "diaper" => services["diaper"],
    "feeding" => services["feeding"],
    "hotwater" => services["hotwater"],
    "address" => address,
    "tel" => tel,
    "website" => website,
    "time" => time,
    "day" => day
  }
end

#http://www.oitakosodate.net/search/suposhop/

urls = []
for i in 1..15 do
  url = "http://www.oitakosodate.net/shoplist/shoplist5name#{i}.html"
  a = open(url)
  mainPage = Nokogiri::HTML(a, nil, 'euc-jp')
  res = parse_list(mainPage)

  urls = urls + res
  sleep(10)
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "http://www.oitakosodate.net/#{a['url']}"
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'euc-jp')
    records << parse_detail(data, a)
    sleep(10)
  rescue
    puts "error"
  end
}

ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list(doc)
  result = []

  resultArea = doc.xpath('//div[@class="Shoplist"]')
  resultArea.each do |area|
    a = area.xpath('./h3//a/@href')
    next if a.text.include?("#")
    next if !a.text.include?("shop")
    
    service = area.xpath('./ul/*').inner_text.strip
    puts service
    feeding = service.include? ("授乳")
    diaper = service.include? ("おむつ替え")
    hotwater = service.include? ("ミルクのお湯")

    next if !(feeding or diaper or hotwater) 
    result << {
      'url' => a.text,
      'feeding' => feeding,
      'diaper' => diaper,
      'hotwater' => hotwater
    }
  end

  result
end

def parse_detail(doc, services)
  #//*[@id="FakeTable"]/div[1]/p
  #//*[@id="DShopName"]/div/h2
  name =doc.xpath('//*[@id="DShopName"]/div/h2').text
  address = doc.xpath('//*[@id="FakeTable"]/div[1]/p').text
  tel = doc.xpath('//*[@id="FakeTable"]/div[2]/p').text
  website = doc.xpath('//*[@id="FakeTable"]/div[3]/p/a').text
  time = doc.xpath('//*[@id="FakeTable"]/div[4]/p').text
  day = doc.xpath('//*[@id="FakeTable"]/div[5]/p').text
  day = "利用不可日:#{day}"

  puts "#{name}/#{address}/#{tel}/#{website}/#{time}/#{day}"
  {
    "name" =>name ,
    "diaper" => services["diaper"],
    "feeding" => services["feeding"],
    "hotwater" => services["hotwater"],
    "address" => address,
    "tel" => tel,
    "website" => website,
    "time" => time,
    "day" => day
  }
end

#http://www.oitakosodate.net/search/suposhop/

urls = []
for i in 1..15 do
  url = "http://www.oitakosodate.net/shoplist/shoplist5name#{i}.html"
  a = open(url)
  mainPage = Nokogiri::HTML(a, nil, 'euc-jp')
  res = parse_list(mainPage)

  urls = urls + res
  sleep(10)
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "http://www.oitakosodate.net/#{a['url']}"
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'euc-jp')
    records << parse_detail(data, a)
    sleep(10)
  rescue
    puts "error"
  end
}

ScraperWiki.save(unique_keys=['name'], data=records)

# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list(doc)
  result = []

  resultArea = doc.xpath('//div[@class="Shoplist"]')
  resultArea.each do |area|
    a = area.xpath('./h3//a/@href')
    next if a.text.include?("#")
    next if !a.text.include?("shop")
    
    service = area.xpath('./ul/*').inner_text.strip
    puts service
    feeding = service.include? ("授乳")
    diaper = service.include? ("おむつ替え")
    hotwater = service.include? ("ミルクのお湯")

    next if !(feeding or diaper or hotwater) 
    result << {
      'url' => a.text,
      'feeding' => feeding,
      'diaper' => diaper,
      'hotwater' => hotwater
    }
  end

  result
end

def parse_detail(doc, services)
  #//*[@id="FakeTable"]/div[1]/p
  #//*[@id="DShopName"]/div/h2
  name =doc.xpath('//*[@id="DShopName"]/div/h2').text
  address = doc.xpath('//*[@id="FakeTable"]/div[1]/p').text
  tel = doc.xpath('//*[@id="FakeTable"]/div[2]/p').text
  website = doc.xpath('//*[@id="FakeTable"]/div[3]/p/a').text
  time = doc.xpath('//*[@id="FakeTable"]/div[4]/p').text
  day = doc.xpath('//*[@id="FakeTable"]/div[5]/p').text
  day = "利用不可日:#{day}"

  puts "#{name}/#{address}/#{tel}/#{website}/#{time}/#{day}"
  {
    "name" =>name ,
    "diaper" => services["diaper"],
    "feeding" => services["feeding"],
    "hotwater" => services["hotwater"],
    "address" => address,
    "tel" => tel,
    "website" => website,
    "time" => time,
    "day" => day
  }
end

#http://www.oitakosodate.net/search/suposhop/

urls = []
for i in 1..15 do
  url = "http://www.oitakosodate.net/shoplist/shoplist5name#{i}.html"
  a = open(url)
  mainPage = Nokogiri::HTML(a, nil, 'euc-jp')
  res = parse_list(mainPage)

  urls = urls + res
  sleep(10)
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "http://www.oitakosodate.net/#{a['url']}"
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'euc-jp')
    records << parse_detail(data, a)
    sleep(10)
  rescue
    puts "error"
  end
}

ScraperWiki.save(unique_keys=['name'], data=records)

