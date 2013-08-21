# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_category(category_id,parent_id)

  appid = "cbb9d8fb2c4ed5e22e0b54f0e39de1ae"
  baseurl = "http://api.rakuten.co.jp/rws/3.0/rest?developerId={appid}&operation=GenreSearch&version=2007-04-11&genreId={category_id}"
  
  url = baseurl.gsub("{appid}", appid)
  url.gsub!("{category_id}", category_id)
  doc = Nokogiri::XML(open(url))
#  p doc

  namespaces = {
    "header" => "http://api.rakuten.co.jp/rws/rest/Header",
    "genreSearch" => "http://api.rakuten.co.jp/rws/rest/GenreSearch/2007-04-11",
  }

  doc.xpath("//current",namespaces).each do |current_node|
    current_data = []
    current_data << {
      'genreId'     => current_node.search("genreId")[0].text,
      'genreName' => current_node.search("genreName")[0].text,
      'genreLevel'    => current_node.search("genreLevel")[0].text,
      'parentId' => parent_id,
    }

    p current_data
    ScraperWiki.save(['genreId', 'genreName', 'genreLevel', 'parentId'], current_data)
  end

  doc.xpath("//child",namespaces).each do |child_node|
    if child_node.search("genreLevel")[0].text.to_i <= 3
       parse_category(child_node.search("genreId")[0].text,category_id)
    end
  end
end

parse_category("0","0")
# doc = Nokogiri::HTML.parse(open(url), 'EUC-JP')
# data = parse_doc(doc)
# (name, furigana) is not unique indeed
# ScraperWiki.save(['name', 'furigana'], data)
