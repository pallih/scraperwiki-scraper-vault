# Blank Ruby


require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.allmusic.com/album/confessions-on-a-dance-floor-mw0000356345/credits"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.



credits = data.css('.creditlist tr a') #.each do |row| # this is with the CSS selector

puts credits

#credits.each do |row|

#puts credits.to_json

#ScraperWiki.save_sqlite(["credits"], row)
#ScraperWiki::save_sqlite(unique_keys=["credits"], data={"row"})

  #end




#a_url = data.xpath('//td/a').map { |link| link['href'] } #----- this part of code would extract only the URL
#t_url = data.xpath('//td/a').map { |text| link['text'] } #----- this part of code would extract only the text


#a_url = data.xpath('//td/a').each { |x| puts "#{x}" } #----- extract each HTML string and print it one under the other 

#a = data.css('div tr td a')myhash=Hash.new(0)
#a = data.xpath('//td/a').map { |link| link['href'] } #----- this part of code would extract only the URL
#b = data.xpath('//td/a').map { |txt| link['text'] }

#a_url = data.xpath('//td/a')


#record = {}        
#record['a_url']= a_url
#ScraperWiki.save_sqlite(["a_url"], record)



#-------------------- alternative code

#array =[] #----- create empty array

#a_url = data.xpath('//td/a')

#b = a_url

#puts b #----- Take this array and print each element one after the other

#puts a_url

# Blank Ruby


require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.allmusic.com/album/confessions-on-a-dance-floor-mw0000356345/credits"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.



credits = data.css('.creditlist tr a') #.each do |row| # this is with the CSS selector

puts credits

#credits.each do |row|

#puts credits.to_json

#ScraperWiki.save_sqlite(["credits"], row)
#ScraperWiki::save_sqlite(unique_keys=["credits"], data={"row"})

  #end




#a_url = data.xpath('//td/a').map { |link| link['href'] } #----- this part of code would extract only the URL
#t_url = data.xpath('//td/a').map { |text| link['text'] } #----- this part of code would extract only the text


#a_url = data.xpath('//td/a').each { |x| puts "#{x}" } #----- extract each HTML string and print it one under the other 

#a = data.css('div tr td a')myhash=Hash.new(0)
#a = data.xpath('//td/a').map { |link| link['href'] } #----- this part of code would extract only the URL
#b = data.xpath('//td/a').map { |txt| link['text'] }

#a_url = data.xpath('//td/a')


#record = {}        
#record['a_url']= a_url
#ScraperWiki.save_sqlite(["a_url"], record)



#-------------------- alternative code

#array =[] #----- create empty array

#a_url = data.xpath('//td/a')

#b = a_url

#puts b #----- Take this array and print each element one after the other

#puts a_url

