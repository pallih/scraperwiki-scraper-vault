# Blank Ruby
require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

njfurl = "http://www.nj.gov/oag/news_2011.html"
news = open(njfurl)
hospdoc = Nokogiri::HTML(news)
# the newslink rows have NJ AG case descriptions
newsitems = hospdoc.search("//td[@class='newslink']")
# we want to iterate through the rows starting with the second row.
newsitems.each_with_index do |item, i|
  if item.text.include? "fraud"
   link = item.search("a/@href")
   strs = item.text.split(' - ')
   date = strs[0].rstrip
   len = date.length - 1
   date = date[0..len] + '/2011'
   event = strs[1] 
   ScraperWiki.save(unique_keys=['Date','Fraud event', 'Link'], data = {'Date' => date,'Fraud event' => event, 'Link' => link})
  end
end
# Blank Ruby
require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

njfurl = "http://www.nj.gov/oag/news_2011.html"
news = open(njfurl)
hospdoc = Nokogiri::HTML(news)
# the newslink rows have NJ AG case descriptions
newsitems = hospdoc.search("//td[@class='newslink']")
# we want to iterate through the rows starting with the second row.
newsitems.each_with_index do |item, i|
  if item.text.include? "fraud"
   link = item.search("a/@href")
   strs = item.text.split(' - ')
   date = strs[0].rstrip
   len = date.length - 1
   date = date[0..len] + '/2011'
   event = strs[1] 
   ScraperWiki.save(unique_keys=['Date','Fraud event', 'Link'], data = {'Date' => date,'Fraud event' => event, 'Link' => link})
  end
end
