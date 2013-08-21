# Blank Ruby
# coding: utf-8


require 'rubygems'
require 'nokogiri'
require 'open-uri'

page = open("http://fukulog.jp/people/coordinate");
html = Nokogiri::HTML(page.read, nil, 'UTF-8');
html_a = html.search('//div[@id="headerMenuBar"]//h3//span')
# html_a = html.search('//span[@class="format-update-date"]') 

puts html_a[0].text

# 結果を保存
result = []
result << {
  'date' => Time.now,
  'coordinateNum' => html_a[0].text
}
ScraperWiki.save(['date'], result)
