# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  doc.xpath('//a').each do |node|
    if node['href'].nil? 
      next
    end

    if node['href'].include?('rds.gnavi.co.jp/food/')
      data = []
      data << {
        'name' => node.text,
        'url' => node['href']
      }
    
      ScraperWiki.save(['name', 'url'], data)
    end
  end
end

url = 'http://rds.gnavi.co.jp/food/'
doc = Nokogiri::HTML.parse(open(url), 'UTF-8')
data = parse_doc(doc)
# ScraperWiki.save(['name', 'furigana'], data)
