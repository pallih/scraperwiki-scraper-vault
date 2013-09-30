# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.
item = data.css('.rankItem-wrap2')

item.each do |var|
  # position
  puts var.at_css('.rankItem-position').text

  # a_name
  puts var.at_css('.rankItem-title').text

  # tags
  puts var.at_css('.rankItem-tags').text

  # blank line to make results prettier
  puts ""

end

 #listeners - puts all the listeners in a list with 150 records

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

 itema = data.css('.rankItem-bar')
 itema.each do |vara|
 puts vara.at_css('.rankItem-bar-percentage').text

  #Alterantive with Xpath
  #data.xpath('//p/span').each do |opt|
  #puts opt.content

end# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.
item = data.css('.rankItem-wrap2')

item.each do |var|
  # position
  puts var.at_css('.rankItem-position').text

  # a_name
  puts var.at_css('.rankItem-title').text

  # tags
  puts var.at_css('.rankItem-tags').text

  # blank line to make results prettier
  puts ""

end

 #listeners - puts all the listeners in a list with 150 records

url = "http://www.last.fm/charts/artists/top/place/all?ending=1169985600&limit=150"

data = Nokogiri::HTML(open(url))

 itema = data.css('.rankItem-bar')
 itema.each do |vara|
 puts vara.at_css('.rankItem-bar-percentage').text

  #Alterantive with Xpath
  #data.xpath('//p/span').each do |opt|
  #puts opt.content

end