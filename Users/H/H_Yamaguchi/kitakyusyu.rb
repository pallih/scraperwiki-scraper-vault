# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_main(doc)
  result = []

  resultArea = doc.xpath('/html/body//*[@class="category-ward"]//a')

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
  name =doc.xpath('//h1[@class="entry-title"]').text.strip
  address = doc.xpath('//*[@class="entry-data-box"]/table//tr[1]/td').inner_text.strip
  tel = doc.xpath('//*[@class="entry-data-box"]/table//tr[2]/td').inner_text.strip
  #fax = doc.xpath('//*[@class="entry-data-box"]/table//tr[3]/td').inner_text.strip
  #time = doc.xpath('//*[@id="contents"]/table//tr[4]/td[2]').inner_text.strip
  #day = doc.xpath('//*[@id="contents"]/table//tr[5]/td[2]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[1]').inner_text.strip
  #diaper = doc.xpath('//*[@id="contents"]/div/table').inner_text.strip
  diaper = ""
  feeding = ""
  doc.xpath('//img').each do |img|
    if img["src"] == "/mapdata/img/eic_babys_jyunyu.png"
      feeding = "○" 
    end 
    if img["src"] == "/mapdata/img/eic_babys_omutsu.png"
      diaper = "○" 
    end 
  end

  #feeding = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[2]').inner_text.strip
  #water = doc.xpath('//*[@id="contents"]/div/table//tr[2]/td[3]').inner_text.strip

  memo = doc.xpath('//*[@class="babystation-about"]').inner_text.strip
  {
    "name" =>name ,
    "address" => address,
    "tel" => tel,
    "diaper" => diaper,
    "feeding" => feeding,
    #"water" => water,
    "memo" => memo
  }
end

url = "http://maps.kosodate-fureai.jp/mapdata/cat94/cat43/"
puts "Fetching #{url}"
mainPage = Nokogiri::HTML.parse(open(url))

urls = parse_main(mainPage)

records = []
puts "url count is #{urls.length}"

urls.each{ |url|
  puts "#{url['url']}"
  data = Nokogiri::HTML.parse(open(url["url"]))
  result = parse_detail(data)
  records << result
  puts "#{result}"
  #break if records.length > 0
  sleep(10)
  
}

ScraperWiki.save(unique_keys=['name'], data=records)

