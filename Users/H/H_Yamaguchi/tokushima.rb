# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_main(doc)
  result = []
  puts doc
  resultArea = doc.xpath('//table[class=list]/tr/td/a')
  #*[@id="contentbody"]/div/table/tbody/tr[2]/td[1]/a
  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//h3').text.strip
  diaper = ""
  feeding = ""
  water = ""
  address = doc.xpath('/html/body/div[3]').inner_text.strip
  tel = doc.xpath('/html/body/div[6]').inner_text.strip
  fax = doc.xpath('/html/body/div[8]').inner_text.strip
  webSite = doc.xpath('/html/body/div[10]').inner_text.strip
  mail = doc.xpath('/html/body/div[12]').inner_text.strip
  memo = "定休日:#{doc.xpath('/html/body/div[14]').inner_text.strip}"
  time = doc.xpath('/html/body/div[16]').inner_text.strip
  doc.xpath('/html/body/div[1]/img').each do |img|
    if img["src"] == "../images/icon04.gif"
      diaper = "○"
    end
    if img["src"] == "../images/icon02.gif"
      feeding = "○"
    end
    if img["src"] == "../images/icon01.gif"
      water = "○"
    end
  end
  puts "#{name}/#{address}/#{tel}/#{fax}/#{webSite}/#{mail}/#{feeding}/#{diaper}/#{water}/#{time}/#{memo}"
  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "fax" => fax,
    "mail" => mail,
    "webSite" => webSite,
    "time" => time,
    "memo" => memo
  }
end

urls = []
for i in 1..1 do
  url = "http://www.pref.tokushima.jp/kodomo/support/result/?page=#{i}&s_keyword=&search=%E6%A4%9C%E7%B4%A2"
  puts "Fetching #{url}"
  html = ScraperWiki::scrape("http://www.pref.tokushima.jp")
  doc = Nokogiri::HTML(html)

  res = parse_main(doc)
  puts "#{res}"
  urls = urls + res
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "xxx"
  puts url
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    sleep(10)
  rescue
    puts "error"
  end
  
}
#puts "#{records}"

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
  puts doc
  resultArea = doc.xpath('//table[class=list]/tr/td/a')
  #*[@id="contentbody"]/div/table/tbody/tr[2]/td[1]/a
  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//h3').text.strip
  diaper = ""
  feeding = ""
  water = ""
  address = doc.xpath('/html/body/div[3]').inner_text.strip
  tel = doc.xpath('/html/body/div[6]').inner_text.strip
  fax = doc.xpath('/html/body/div[8]').inner_text.strip
  webSite = doc.xpath('/html/body/div[10]').inner_text.strip
  mail = doc.xpath('/html/body/div[12]').inner_text.strip
  memo = "定休日:#{doc.xpath('/html/body/div[14]').inner_text.strip}"
  time = doc.xpath('/html/body/div[16]').inner_text.strip
  doc.xpath('/html/body/div[1]/img').each do |img|
    if img["src"] == "../images/icon04.gif"
      diaper = "○"
    end
    if img["src"] == "../images/icon02.gif"
      feeding = "○"
    end
    if img["src"] == "../images/icon01.gif"
      water = "○"
    end
  end
  puts "#{name}/#{address}/#{tel}/#{fax}/#{webSite}/#{mail}/#{feeding}/#{diaper}/#{water}/#{time}/#{memo}"
  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "fax" => fax,
    "mail" => mail,
    "webSite" => webSite,
    "time" => time,
    "memo" => memo
  }
end

urls = []
for i in 1..1 do
  url = "http://www.pref.tokushima.jp/kodomo/support/result/?page=#{i}&s_keyword=&search=%E6%A4%9C%E7%B4%A2"
  puts "Fetching #{url}"
  html = ScraperWiki::scrape("http://www.pref.tokushima.jp")
  doc = Nokogiri::HTML(html)

  res = parse_main(doc)
  puts "#{res}"
  urls = urls + res
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "xxx"
  puts url
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    sleep(10)
  rescue
    puts "error"
  end
  
}
#puts "#{records}"

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
  puts doc
  resultArea = doc.xpath('//table[class=list]/tr/td/a')
  #*[@id="contentbody"]/div/table/tbody/tr[2]/td[1]/a
  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//h3').text.strip
  diaper = ""
  feeding = ""
  water = ""
  address = doc.xpath('/html/body/div[3]').inner_text.strip
  tel = doc.xpath('/html/body/div[6]').inner_text.strip
  fax = doc.xpath('/html/body/div[8]').inner_text.strip
  webSite = doc.xpath('/html/body/div[10]').inner_text.strip
  mail = doc.xpath('/html/body/div[12]').inner_text.strip
  memo = "定休日:#{doc.xpath('/html/body/div[14]').inner_text.strip}"
  time = doc.xpath('/html/body/div[16]').inner_text.strip
  doc.xpath('/html/body/div[1]/img').each do |img|
    if img["src"] == "../images/icon04.gif"
      diaper = "○"
    end
    if img["src"] == "../images/icon02.gif"
      feeding = "○"
    end
    if img["src"] == "../images/icon01.gif"
      water = "○"
    end
  end
  puts "#{name}/#{address}/#{tel}/#{fax}/#{webSite}/#{mail}/#{feeding}/#{diaper}/#{water}/#{time}/#{memo}"
  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "fax" => fax,
    "mail" => mail,
    "webSite" => webSite,
    "time" => time,
    "memo" => memo
  }
end

urls = []
for i in 1..1 do
  url = "http://www.pref.tokushima.jp/kodomo/support/result/?page=#{i}&s_keyword=&search=%E6%A4%9C%E7%B4%A2"
  puts "Fetching #{url}"
  html = ScraperWiki::scrape("http://www.pref.tokushima.jp")
  doc = Nokogiri::HTML(html)

  res = parse_main(doc)
  puts "#{res}"
  urls = urls + res
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "xxx"
  puts url
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    sleep(10)
  rescue
    puts "error"
  end
  
}
#puts "#{records}"

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
  puts doc
  resultArea = doc.xpath('//table[class=list]/tr/td/a')
  #*[@id="contentbody"]/div/table/tbody/tr[2]/td[1]/a
  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    result << {
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//h3').text.strip
  diaper = ""
  feeding = ""
  water = ""
  address = doc.xpath('/html/body/div[3]').inner_text.strip
  tel = doc.xpath('/html/body/div[6]').inner_text.strip
  fax = doc.xpath('/html/body/div[8]').inner_text.strip
  webSite = doc.xpath('/html/body/div[10]').inner_text.strip
  mail = doc.xpath('/html/body/div[12]').inner_text.strip
  memo = "定休日:#{doc.xpath('/html/body/div[14]').inner_text.strip}"
  time = doc.xpath('/html/body/div[16]').inner_text.strip
  doc.xpath('/html/body/div[1]/img').each do |img|
    if img["src"] == "../images/icon04.gif"
      diaper = "○"
    end
    if img["src"] == "../images/icon02.gif"
      feeding = "○"
    end
    if img["src"] == "../images/icon01.gif"
      water = "○"
    end
  end
  puts "#{name}/#{address}/#{tel}/#{fax}/#{webSite}/#{mail}/#{feeding}/#{diaper}/#{water}/#{time}/#{memo}"
  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "fax" => fax,
    "mail" => mail,
    "webSite" => webSite,
    "time" => time,
    "memo" => memo
  }
end

urls = []
for i in 1..1 do
  url = "http://www.pref.tokushima.jp/kodomo/support/result/?page=#{i}&s_keyword=&search=%E6%A4%9C%E7%B4%A2"
  puts "Fetching #{url}"
  html = ScraperWiki::scrape("http://www.pref.tokushima.jp")
  doc = Nokogiri::HTML(html)

  res = parse_main(doc)
  puts "#{res}"
  urls = urls + res
end


records = []
puts "url count is #{urls.length}"

urls.each{ |a|
  url = "xxx"
  puts url
  begin
    data = Nokogiri::HTML.parse(open(url), nil, 'utf-8')
    records << parse_detail(data)
    sleep(10)
  rescue
    puts "error"
  end
  
}
#puts "#{records}"

ScraperWiki.save(unique_keys=['name'], data=records)

