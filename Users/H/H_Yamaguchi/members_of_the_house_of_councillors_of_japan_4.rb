# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

 resultArea = doc.xpath('/html/body//div[@class="search_result_table"]')[0]

  # Note tr[1] is actually a table header
  resultArea.xpath('table').each do |table|
    name = table.xpath('.//td[@class="shop_name"]/a').map do |a|
      field = a.text 
      field
    end
    name = name.first

    address = table.xpath('.//tr[1]/td[3]/text()').to_s


    tel = table.xpath('.//tr[2]/td[1]/text()').to_s
    
    fax = table.xpath('.//tr[2]/td[2]/text()').to_s

    
    equipments = table.xpath('.//tr[4]/td[1]/span').map do |td|
      td.text
    end
    diaper, feeding, others, _ = equipments

    puts "#{name},#{address},#{tel},#{fax},#{feeding},#{diaper},#{others}"
    if !name.nil? then
      result << {
        'name'     => name,
        'address' => address,
        'tel' => tel,
        'fax' => fax,
        'diaper' => diaper,
        'feeding' => feeding,
        'others' => others
      }
    end
  end

  result
end

for i in 0..86
  ds = i * 30
  url = "http://kosodate.asvssl.net/cgi-bin/yuutai/yuutai.cgi?ds=#{ds}&baby=baby01+baby02&count=0&mode=1#"
  puts "Fetching #{url}"
  sleep 10
  doc = Nokogiri::HTML.parse(open(url))
  data = parse_doc(doc)
  ScraperWiki.save(unique_keys=['name'], data=data)
end
