# Blank Ruby


require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.allmusic.com/album/confessions-on-a-dance-floor-mw0000356345/credits"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.



credits = data.css('.name-credit')
names = data.css('.name primary_link')
#rdate = data.css('release-date')
#genre = data.xpath('//*[@id="sidebar"]/dl/dd[3]/ul/li')
#styles = data.xpath('//*[@id="sidebar"]/dl/dd[4]/ul/li').each do |styles|

puts names
puts credits


#moods = data.xpath('//*[@id="sidebar"]/div[4]/ul/li')
#themes = data.xpath('//*[@id="sidebar"]/div[5]/ul/li')






#--------------------------
#test code and other code

#credits = data.css('.creditlist tr a')

#data = {
                    #'RDATE' : rdate,
                    #'CREDITS' : credits,
                    #'GENRE' : genre,
                    #'STYLES' : styles,
                    #'MOODS' : moods,
                    #'THEMES' : themes,
                        #}
                #scraperwiki.sqlite.save(unique_keys=['STYLES'], data=data)
                #scraperwiki.sqlite.save(unique_keys=['RDATE','CREDITS','GENRE','STYLES','MOODS','THEMES'], data=data)
# end# Blank Ruby


require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.allmusic.com/album/confessions-on-a-dance-floor-mw0000356345/credits"

data = Nokogiri::HTML(open(url))

# Here is where we use the new method to create an object that holds all the
# concert listings.  Think of it as an array that we can loop through.  It's
# not an array, but it does respond very similarly.



credits = data.css('.name-credit')
names = data.css('.name primary_link')
#rdate = data.css('release-date')
#genre = data.xpath('//*[@id="sidebar"]/dl/dd[3]/ul/li')
#styles = data.xpath('//*[@id="sidebar"]/dl/dd[4]/ul/li').each do |styles|

puts names
puts credits


#moods = data.xpath('//*[@id="sidebar"]/div[4]/ul/li')
#themes = data.xpath('//*[@id="sidebar"]/div[5]/ul/li')






#--------------------------
#test code and other code

#credits = data.css('.creditlist tr a')

#data = {
                    #'RDATE' : rdate,
                    #'CREDITS' : credits,
                    #'GENRE' : genre,
                    #'STYLES' : styles,
                    #'MOODS' : moods,
                    #'THEMES' : themes,
                        #}
                #scraperwiki.sqlite.save(unique_keys=['STYLES'], data=data)
                #scraperwiki.sqlite.save(unique_keys=['RDATE','CREDITS','GENRE','STYLES','MOODS','THEMES'], data=data)
# end