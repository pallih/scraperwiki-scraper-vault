# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  link = doc.xpath('//a')
  link.each do |a|
    p a.to_s
  end

  result
end

def parse_category(category_id, depth)
  namespaces = {
    "categorySearch" => "urn:yahoo:jp:categorySearch"
  }

  appid = "34W6mp6xg65CaJTq8Tyt96rpQdo25_GI2NtKiVAVIM91ppyRvwH73I3OetPC38C4NA--"
  baseurl = "http://shopping.yahooapis.jp/ShoppingWebService/V1/categorySearch?appid={appid}&category_id={category_id}"
  
  url = baseurl.gsub("{appid}", appid)
  url.gsub!("{category_id}", category_id)
  doc = Nokogiri::XML(open(url))
  p doc
  doc.xpath("//categorySearch:Current",namespaces).each do |current_node|
    current_data = []
    current_data << {
      'Id'     => current_node.search("Id")[0].text,
      'ParentId' => current_node.search("ParentId")[0].text,
      'Url'    => current_node.search("Url")[0].text,
      'Short' => current_node.search("Short")[0].text,
      'Depth' => depth,
    }

    ScraperWiki.save(['Id', 'ParentId', 'Url', 'Short'], current_data)
  end

  if depth > 2
    return
  end

  doc.xpath("//categorySearch:Child",namespaces).each do |child_node|
    p child_node.search("Id")[0].text
    parse_category(child_node.search("Id")[0].text, depth+1)
  end
end

parse_category("1", 1)
# doc = Nokogiri::HTML.parse(open(url), 'EUC-JP')
# data = parse_doc(doc)
# (name, furigana) is not unique indeed
# ScraperWiki.save(['name', 'furigana'], data)
