require 'nokogiri'
require 'open-uri'

page = Nokogiri::HTML(open("http://dreamteam.afl.com.au/?p=topplayers"))   

p page.xpath('//table[@class="data"]/tr/td')[2]

#.each do |player|

#  player.text

#endrequire 'nokogiri'
require 'open-uri'

page = Nokogiri::HTML(open("http://dreamteam.afl.com.au/?p=topplayers"))   

p page.xpath('//table[@class="data"]/tr/td')[2]

#.each do |player|

#  player.text

#end