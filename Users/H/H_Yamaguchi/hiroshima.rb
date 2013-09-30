# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_main(doc)
  result = []

  resultArea = doc.xpath('/html/body//table//a')

  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    result << {
      'name'     => a.text,
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="title"]').text.strip
  diaper = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[1]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table').inner_text.strip
  feeding = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[2]').inner_text.strip
  water = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[3]').inner_text.strip
  address = doc.xpath('//*[@id="contents"]/table//tr[2]/td[2]').inner_text.strip
  tel = doc.xpath('//*[@id="contents"]/table//tr[3]/td[2]').inner_text.strip
  time = doc.xpath('//*[@id="contents"]/table//tr[4]/td[2]').inner_text.strip
  day = doc.xpath('//*[@id="contents"]/table//tr[5]/td[2]').inner_text.strip

  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "time" => time,
    "day" => day
  }
end

url = "http://www.city.hiroshima.lg.jp/www/contents/0000000000000/1327907085933/index.html"
puts "Fetching #{url}"
mainPage = Nokogiri::HTML.parse(open(url))

urls = parse_main(mainPage)

records = []
puts "url count is #{urls.length}"

urls.each{ |url|
  puts "#{url}"
  data = Nokogiri::HTML.parse(open(url["url"]))
  records << parse_detail(data)
  sleep(10)
}
puts "#{records}"

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

  resultArea = doc.xpath('/html/body//table//a')

  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    result << {
      'name'     => a.text,
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="title"]').text.strip
  diaper = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[1]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table').inner_text.strip
  feeding = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[2]').inner_text.strip
  water = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[3]').inner_text.strip
  address = doc.xpath('//*[@id="contents"]/table//tr[2]/td[2]').inner_text.strip
  tel = doc.xpath('//*[@id="contents"]/table//tr[3]/td[2]').inner_text.strip
  time = doc.xpath('//*[@id="contents"]/table//tr[4]/td[2]').inner_text.strip
  day = doc.xpath('//*[@id="contents"]/table//tr[5]/td[2]').inner_text.strip

  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "time" => time,
    "day" => day
  }
end

url = "http://www.city.hiroshima.lg.jp/www/contents/0000000000000/1327907085933/index.html"
puts "Fetching #{url}"
mainPage = Nokogiri::HTML.parse(open(url))

urls = parse_main(mainPage)

records = []
puts "url count is #{urls.length}"

urls.each{ |url|
  puts "#{url}"
  data = Nokogiri::HTML.parse(open(url["url"]))
  records << parse_detail(data)
  sleep(10)
}
puts "#{records}"

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

  resultArea = doc.xpath('/html/body//table//a')

  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    result << {
      'name'     => a.text,
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="title"]').text.strip
  diaper = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[1]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table').inner_text.strip
  feeding = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[2]').inner_text.strip
  water = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[3]').inner_text.strip
  address = doc.xpath('//*[@id="contents"]/table//tr[2]/td[2]').inner_text.strip
  tel = doc.xpath('//*[@id="contents"]/table//tr[3]/td[2]').inner_text.strip
  time = doc.xpath('//*[@id="contents"]/table//tr[4]/td[2]').inner_text.strip
  day = doc.xpath('//*[@id="contents"]/table//tr[5]/td[2]').inner_text.strip

  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "time" => time,
    "day" => day
  }
end

url = "http://www.city.hiroshima.lg.jp/www/contents/0000000000000/1327907085933/index.html"
puts "Fetching #{url}"
mainPage = Nokogiri::HTML.parse(open(url))

urls = parse_main(mainPage)

records = []
puts "url count is #{urls.length}"

urls.each{ |url|
  puts "#{url}"
  data = Nokogiri::HTML.parse(open(url["url"]))
  records << parse_detail(data)
  sleep(10)
}
puts "#{records}"

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

  resultArea = doc.xpath('/html/body//table//a')

  # Note tr[1] is actually a table header
  resultArea.each do |a|
    next if a["href"].nil? 
    next if a["href"].include?("#")
    result << {
      'name'     => a.text,
      'url' => a["href"]
    }
  end

  result
end

def parse_detail(doc)
  name =doc.xpath('//*[@id="title"]').text.strip
  diaper = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[1]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table').inner_text.strip
  feeding = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[2]').inner_text.strip
  water = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[3]').inner_text.strip
  address = doc.xpath('//*[@id="contents"]/table//tr[2]/td[2]').inner_text.strip
  tel = doc.xpath('//*[@id="contents"]/table//tr[3]/td[2]').inner_text.strip
  time = doc.xpath('//*[@id="contents"]/table//tr[4]/td[2]').inner_text.strip
  day = doc.xpath('//*[@id="contents"]/table//tr[5]/td[2]').inner_text.strip

  {
    "name" =>name ,
    "diaper" => diaper,
    "feeding" => feeding,
    "water" => water,
    "address" => address,
    "tel" => tel,
    "time" => time,
    "day" => day
  }
end

url = "http://www.city.hiroshima.lg.jp/www/contents/0000000000000/1327907085933/index.html"
puts "Fetching #{url}"
mainPage = Nokogiri::HTML.parse(open(url))

urls = parse_main(mainPage)

records = []
puts "url count is #{urls.length}"

urls.each{ |url|
  puts "#{url}"
  data = Nokogiri::HTML.parse(open(url["url"]))
  records << parse_detail(data)
  sleep(10)
}
puts "#{records}"

ScraperWiki.save(unique_keys=['name'], data=records)

