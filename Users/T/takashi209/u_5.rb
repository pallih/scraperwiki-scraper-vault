# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

#if RUBY_VERSION < '1.9.0'
#  $KCODE = 'UTF8'
#end

def parse_doc(doc)
  # カテゴリの取得
  doc.xpath("//div[@id='itemcategory_list']//a").each do |node|
    data= []
    data << {
      'name' => node.text,
      'url' => node['href']
    }

#    p data
    ScraperWiki.save(['name', 'url'], data)
  end
end

url = 'http://calamel.jp/?act=cat_list'
doc = Nokogiri::HTML.parse(open(url), 'EUC')
data = parse_doc(doc)
