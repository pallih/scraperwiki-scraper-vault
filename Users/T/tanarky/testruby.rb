# -*- coding: utf-8 -*-
 
require 'rubygems'
require 'mechanize'
require 'open-uri'
require 'nokogiri'

agent = Mechanize.new
agent.get('http://shopping.yahoo.co.jp/')
names = agent.page.root.search('#YshpMdFirstLayerCategory div li a')

names.each do |n|
  data = []
  data << {
    'name' => n.inner_text
  }
  ScraperWiki.save(['name'],data)
end
