# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.

position = []
a_name = []
tags = []
listeners = []
combine = []

char1 = "_"
 
  # position
  position = [data.css('.rankItem-position').text]

  # a_name
  a_name = [data.css('.rankItem-title').text]
  
  # tags
  tags = [data.css('.rankItem-tags').text]

  # Listeners
  listeners = [data.css('.rankItem-bar-percentage').text]
  #listeners = [data.xpath('//p/span')]
 
combine = [position,a_name,tags,listeners]
 
#combine = position + char1 + a_name + char1 + tags + char1 + listeners

a_name.each do |opt|
puts opt
end

#puts combine

 #listeners - puts all the listeners in a list with 150 records

#url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

#data = Nokogiri::HTML(open(url))

 #itema = data.css('.rankItem-bar')
 #itema.each do |vara|
 #puts vara.at_css('.rankItem-bar-percentage').text

  #Alterantive with Xpath
  #data.xpath('//p/span').each do |opt|
  #puts opt.content

# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.

position = []
a_name = []
tags = []
listeners = []
combine = []

char1 = "_"
 
  # position
  position = [data.css('.rankItem-position').text]

  # a_name
  a_name = [data.css('.rankItem-title').text]
  
  # tags
  tags = [data.css('.rankItem-tags').text]

  # Listeners
  listeners = [data.css('.rankItem-bar-percentage').text]
  #listeners = [data.xpath('//p/span')]
 
combine = [position,a_name,tags,listeners]
 
#combine = position + char1 + a_name + char1 + tags + char1 + listeners

a_name.each do |opt|
puts opt
end

#puts combine

 #listeners - puts all the listeners in a list with 150 records

#url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

#data = Nokogiri::HTML(open(url))

 #itema = data.css('.rankItem-bar')
 #itema.each do |vara|
 #puts vara.at_css('.rankItem-bar-percentage').text

  #Alterantive with Xpath
  #data.xpath('//p/span').each do |opt|
  #puts opt.content

