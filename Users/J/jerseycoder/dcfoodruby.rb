require 'rss/2.0'
 require 'date'
 require 'nokogiri'
 require 'open-uri'
   
feedData = ScraperWiki.scrape("http://creatorexport.zoho.com/showRss.do?viewlinkId=3&fileType=rss&link=true&complete=true&sharedBy=dcfoodfinder")
doc = Nokogiri::XML(feedData)
items = doc.xpath('//item', 'zc' => 'http://creator.zoho.com/rss/')


items.each do |item|
  #if item.xpath('//zc:resourceServices', 'zc' => 'http://creator.zoho.com/rss/').text == 'Free Meals'
     puts item.xpath('//zc:resourceServices', 'zc' => 'http://creator.zoho.com/rss/').text
  #end
endrequire 'rss/2.0'
 require 'date'
 require 'nokogiri'
 require 'open-uri'
   
feedData = ScraperWiki.scrape("http://creatorexport.zoho.com/showRss.do?viewlinkId=3&fileType=rss&link=true&complete=true&sharedBy=dcfoodfinder")
doc = Nokogiri::XML(feedData)
items = doc.xpath('//item', 'zc' => 'http://creator.zoho.com/rss/')


items.each do |item|
  #if item.xpath('//zc:resourceServices', 'zc' => 'http://creator.zoho.com/rss/').text == 'Free Meals'
     puts item.xpath('//zc:resourceServices', 'zc' => 'http://creator.zoho.com/rss/').text
  #end
end