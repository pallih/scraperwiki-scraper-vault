# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_list_page(doc)
  result = []
  anchors = doc.xpath('//*[@id="main"]//tr[1]/td[2]/a')

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
  name =doc.xpath('//*[@class="shop_detail"]/tr[2]/td/p').text
  address = doc.xpath('//*[@class="shop_detail"]/tr[3]/td').text
  day = doc.xpath('//*[@class="shop_detail"]/tr[4]/td').text
  time = doc.xpath('//*[@class="shop_detail"]/tr[5]/td').text
  tel = doc.xpath('//*[@class="shop_detail"]/tr[7]/td').text
  fax = doc.xpath('//*[@class="shop_detail"]/tr[8]/td').text
  website = doc.xpath('//*[@class="shop_detail"]/tr[9]/td').text
  email = doc.xpath('//*[@class="shop_detail"]/tr[10]/td').text

  services = doc.xpath('//*[@id="middle_shadow"]/table/tbody/tr[2]/td/div[3]/table/tr[1]/td[2]').text
  services += doc.xpath('//*[@id="middle_shadow"]/table/tbody/tr[2]/td/div[4]/table/tr[1]/td[2]').text
  feeding = ""
  diaper = ""
  hotwater = ""
  feeding = "○" unless services.index("授乳スペース").nil? 
  diaper = "○" unless services.index("オムツ交換コーナー").nil? 
  hotwater = "○" unless services.index("ミルクのお湯").nil? 
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
for i in 1..188 do
#for i in 1..1 do
  url = "http://www.ehime-nobinobi.com/ouentai/list/SearchList.php?page=#{i}"
  listPage = open(url)
  doc = Nokogiri::HTML(listPage, nil, 'shift_jis')
  res = parse_list_page(doc)
  urls = urls + res
  sleep(10)
end


records = []
puts "url count is #{urls.length}"

ScraperWiki.save(unique_keys=['url'], data=urls)

#urls.each{ |a|
#  url = "http://www.ehime-nobinobi.com/ouentai/list/#{a['url']}"
#    data = Nokogiri::HTML.parse(open(url), nil, 'shift_jis')
#    records << parse_detail(data)
#    sleep(10)  
#}
#puts "#{records}"

#ScraperWiki.save(unique_keys=['name'], data=records)
