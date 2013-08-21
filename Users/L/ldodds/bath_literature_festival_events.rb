# Bath Music Festival Event Scraper
#
#
# Note: currently failing to parse 6 events because of priblem parsing this page:
# http://www.bathmusicfest.org.uk/events.aspx?p=3&t=&v=&d=&y=2012&s=d&a=
require 'nokogiri'           
require 'date'

pages = ["http://www.bathmusicfest.org.uk/events.aspx"]

page = Nokogiri::HTML( ScraperWiki.scrape( pages[0] ) )
page.search("#col2 a").each do |link|
  if ( link["title"] && link["title"].match("Page") && link["href"].match("events.aspx") )
    pages << "http://www.bathmusicfest.org.uk/#{link["href"]}"
  end
end

pages.each do |url|
  puts "processing #{url}"
  #FIXME broken html on this page?
  #url ="http://www.bathmusicfest.org.uk/events.aspx?p=3&t=&v=&d=&y=2012&s=d&a="
  to_scrape = Nokogiri::HTML( ScraperWiki.scrape( url ) )
  to_scrape.search("#col2 div[style='width:155px; float:left;'] span").each do |d|
   #Tuesday 27 Mar, 1.00pm 
   if d.children[4]
     datetime = DateTime.strptime( d.children[4].content, "%A %e %b, %k.%M%P" )
     slug = d.children[0]["href"].split(".")[0] 
     event = {
       "id" => "#{slug}_#{datetime.to_time.to_i}",
       "page" => "http://www.bathmusicfest.org.uk/#{d.children[0]["href"]}",
       "title" => event_title = d.children[0].content,
       "venue" => d.children[2].content,
       "date" => datetime
     }
     ScraperWiki.save_sqlite(unique_keys=['id'], data=event) 
   end
  end 
end