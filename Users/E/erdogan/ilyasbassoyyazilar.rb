require 'open-uri'
require 'mechanize'
require 'rss/maker'
require "json"

version = "2.0" # ["0.9", "1.0", "2.0"]
today = Time.now
date = "&year=" + today.year.to_s + "&month=" + today.month.to_s + "&day=" + today.day.to_s 

rss = RSS::Maker.make(version) do |m|
  m.channel.title = "Ilyas Bassoy Yazilari"
  m.channel.link = "http://www.birgun.net/writer_index.php?category_code=1231167572&news_code=1323700883" + date
  m.channel.description = "Ilyas Bassoy'un Birgun gazetesinde yayimlanan yazilari"
  
  # Retrieve page
  agent = Mechanize.new
  page = agent.get(m.channel.link)
  hrefs = []
  
  page.links.each do |link|
    if link.attributes[:class] =~ /toollinks/ && link.href.include?("1231167572") 
      unless hrefs.include?(link.href)
        hrefs.push link.href
        i = m.items.new_item
        i.title = link
        i.link = link.href
        # get date
        year = link.href.split('year=')[1].split('&month')[0]
        month = link.href.split('month=')[1].split('&day')[0]
        day = link.href.split('day=')[1].split('"')[0]
        d = Time.parse(year+'-'+month+'-'+day)
        i.pubDate = d
      end
    end
  end
  m.items.do_sort = true
end

ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

puts rss

require 'open-uri'
require 'mechanize'
require 'rss/maker'
require "json"

version = "2.0" # ["0.9", "1.0", "2.0"]
today = Time.now
date = "&year=" + today.year.to_s + "&month=" + today.month.to_s + "&day=" + today.day.to_s 

rss = RSS::Maker.make(version) do |m|
  m.channel.title = "Ilyas Bassoy Yazilari"
  m.channel.link = "http://www.birgun.net/writer_index.php?category_code=1231167572&news_code=1323700883" + date
  m.channel.description = "Ilyas Bassoy'un Birgun gazetesinde yayimlanan yazilari"
  
  # Retrieve page
  agent = Mechanize.new
  page = agent.get(m.channel.link)
  hrefs = []
  
  page.links.each do |link|
    if link.attributes[:class] =~ /toollinks/ && link.href.include?("1231167572") 
      unless hrefs.include?(link.href)
        hrefs.push link.href
        i = m.items.new_item
        i.title = link
        i.link = link.href
        # get date
        year = link.href.split('year=')[1].split('&month')[0]
        month = link.href.split('month=')[1].split('&day')[0]
        day = link.href.split('day=')[1].split('"')[0]
        d = Time.parse(year+'-'+month+'-'+day)
        i.pubDate = d
      end
    end
  end
  m.items.do_sort = true
end

ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

puts rss

