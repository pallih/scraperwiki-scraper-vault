require 'rss/2.0'
require 'date'
require 'nokogiri'
require 'open-uri'
   
feedData = ScraperWiki.scrape("http://creatorexport.zoho.com/showRss.do?viewlinkId=3&fileType=rss&link=true&complete=true&sharedBy=dcfoodfinder")
nsCtx = {"zc" => "http://creator.zoho.com/rss/"}

doc = Nokogiri::XML(feedData)
items = doc.xpath('//item', nsCtx)

items.each do |item|
  val = item.xpath('zc:resourceServices', nsCtx).text
  if (val.to_s =~ /Free Meal/)    # wish [contains(text(), "Free Meal")] was supported in the Nokogiri xpath
    record = {
      'title' => item.xpath('title').text,
      'services' => val,
      'organization' => item.xpath('zc:organization', nsCtx).text,
      'latitude' => item.xpath('zc:latitude', nsCtx).text,
      'longitude' => item.xpath('zc:longitude', nsCtx).text
     }
puts record
     #ScraperWiki.save(['title'], record)
  end
end
require 'rss/2.0'
require 'date'
require 'nokogiri'
require 'open-uri'
   
feedData = ScraperWiki.scrape("http://creatorexport.zoho.com/showRss.do?viewlinkId=3&fileType=rss&link=true&complete=true&sharedBy=dcfoodfinder")
nsCtx = {"zc" => "http://creator.zoho.com/rss/"}

doc = Nokogiri::XML(feedData)
items = doc.xpath('//item', nsCtx)

items.each do |item|
  val = item.xpath('zc:resourceServices', nsCtx).text
  if (val.to_s =~ /Free Meal/)    # wish [contains(text(), "Free Meal")] was supported in the Nokogiri xpath
    record = {
      'title' => item.xpath('title').text,
      'services' => val,
      'organization' => item.xpath('zc:organization', nsCtx).text,
      'latitude' => item.xpath('zc:latitude', nsCtx).text,
      'longitude' => item.xpath('zc:longitude', nsCtx).text
     }
puts record
     #ScraperWiki.save(['title'], record)
  end
end
