# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

page = open("http://fukulog.jp/people/coordinate");
html = Nokogiri::HTML(page.read, nil, 'UTF-8');
html_a = html.search('//span[@class="format-update-date"]')
html_a.each_with_index do |a, i|
  puts a
end


# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

page = open("http://fukulog.jp/people/coordinate");
html = Nokogiri::HTML(page.read, nil, 'UTF-8');
html_a = html.search('//span[@class="format-update-date"]')
html_a.each_with_index do |a, i|
  puts a
end


