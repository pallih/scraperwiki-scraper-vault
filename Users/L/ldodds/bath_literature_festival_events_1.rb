# Bath Literature Festival Event Scraper
#
#
# Note: still testing
# Currently missing ~18 events
require 'nokogiri'           
require 'date'
require 'open-uri'

pages = ["http://www.bathlitfest.org.uk/events.aspx"]

page = Nokogiri::HTML( open( pages[0] ) )
puts page.content
page.search("#col2 a").each do |link|
  if ( link["title"] && link["title"].match("Page") && link["href"].match("events.aspx") )
    pages << "http://www.bathlitfest.org.uk/#{link["href"]}"
  end
end

pages.each do |url|
  puts "processing #{url}"
  to_scrape = Nokogiri::HTML( ScraperWiki.scrape( url ) )
  to_scrape.search("#col2 div[style='width:155px; float:left;'] span").each do |d|
   #Tuesday 27 Mar, 1.00pm 
   if d.children[4]
     if d.children[4].content.include?(",")
       datetime = DateTime.strptime( d.children[4].content, "%A %e %b, %k.%M%P" )       
     else
       datetime = DateTime.strptime( d.children[4].content, "%A %e %b" )
     end
     slug = d.children[0]["href"].split(".")[0] 
     event = {
       "id" => "#{slug}_#{datetime.to_time.to_i}",
       "page" => "http://www.bathlitfest.org.uk/#{d.children[0]["href"]}",
       "title" => event_title = d.children[0].content,
       "venue" => d.children[2].content,
       "date" => datetime
     }
     ScraperWiki.save_sqlite(unique_keys=['id'], data=event) 
   end
  end 
end# Bath Literature Festival Event Scraper
#
#
# Note: still testing
# Currently missing ~18 events
require 'nokogiri'           
require 'date'
require 'open-uri'

pages = ["http://www.bathlitfest.org.uk/events.aspx"]

page = Nokogiri::HTML( open( pages[0] ) )
puts page.content
page.search("#col2 a").each do |link|
  if ( link["title"] && link["title"].match("Page") && link["href"].match("events.aspx") )
    pages << "http://www.bathlitfest.org.uk/#{link["href"]}"
  end
end

pages.each do |url|
  puts "processing #{url}"
  to_scrape = Nokogiri::HTML( ScraperWiki.scrape( url ) )
  to_scrape.search("#col2 div[style='width:155px; float:left;'] span").each do |d|
   #Tuesday 27 Mar, 1.00pm 
   if d.children[4]
     if d.children[4].content.include?(",")
       datetime = DateTime.strptime( d.children[4].content, "%A %e %b, %k.%M%P" )       
     else
       datetime = DateTime.strptime( d.children[4].content, "%A %e %b" )
     end
     slug = d.children[0]["href"].split(".")[0] 
     event = {
       "id" => "#{slug}_#{datetime.to_time.to_i}",
       "page" => "http://www.bathlitfest.org.uk/#{d.children[0]["href"]}",
       "title" => event_title = d.children[0].content,
       "venue" => d.children[2].content,
       "date" => datetime
     }
     ScraperWiki.save_sqlite(unique_keys=['id'], data=event) 
   end
  end 
end