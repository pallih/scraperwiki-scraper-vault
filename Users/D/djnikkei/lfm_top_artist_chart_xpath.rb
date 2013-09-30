# Blank Ruby

require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

#Listeners

listeners = data.xpath('//p/span')

listeners.each do |opt|

puts opt.content

end# Blank Ruby

require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

#Listeners

listeners = data.xpath('//p/span')

listeners.each do |opt|

puts opt.content

end