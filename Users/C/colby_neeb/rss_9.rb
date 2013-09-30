require 'rss/2.0'
require 'rss/maker'
require 'date'

# # Return any ScraperWiki database as an RSS feed
#
# # Usage
# 
# http://scraperwikiviews.com/run/rss_2/?scraper=<name of scraper>[&params]
#
# Available params:
#
# table => name of the scraper's table to query
# limit => maximum number of entries to return
# order => name of column to order by (DESC)
# title => name of the column to use as entry title
# link => name of the column to use as entry link
# date => name of the column to use as entry date
#         May be a Time,String or Numeric column
# desc => name of the column to use as entry content ("description")
#
#
# Examples
#
# http://scraperwikiviews.com/run/rss_2/?scraper=alertbox
# http://scraperwikiviews.com/run/rss_2/?scraper=communication_log&link=uri&date=date_submitted_c&title=behalf&table=contact&order=date_submitted_c  

ScraperWiki.httpresponseheader('Content-Type', 'application/rss_xml')

query_string = ENV["QUERY_STRING"]

raise "Missing QUERY_STRING" if query_string.nil? 

params = query_string.split("&").inject({}) do |memo, p|
  key, val = p.split("=")
  memo[key]= val
  memo
end

raise "Missing 'scraper' param" unless params["scraper"]

scraper = params["scraper"]
title = params["title"] || "title"
link = params["link"] || "link"
description = params["desc"] || "description"
date = params["date"] || "date"

table = params["table"] || "swdata"
limit = params["limit"] || 20
order = params["order"] || date

raise unless scraper

ScraperWiki.attach(scraper)
data = ScraperWiki.select("* from #{table} order by #{order} desc limit #{limit}")

rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = scraper
  m.channel.link = "https://scraperwiki.com/scrapers/%s"% params["scraper"]
  m.channel.description = "RSS feed from ScraperWiki - %s" % params["scraper"]

  data.each do |entry|
    item = m.items.new_item
    item.title = entry[title] || ""
    item.link = entry[link] || ""
    item.description = entry[description] || ""
    item.date = case entry[date]
        when Numeric then Time.at(entry[date])
        when Time then entry[date]
        when String then Time.parse(entry[date]) 
        else Time.new
      end
  end
end

puts rssrequire 'rss/2.0'
require 'rss/maker'
require 'date'

# # Return any ScraperWiki database as an RSS feed
#
# # Usage
# 
# http://scraperwikiviews.com/run/rss_2/?scraper=<name of scraper>[&params]
#
# Available params:
#
# table => name of the scraper's table to query
# limit => maximum number of entries to return
# order => name of column to order by (DESC)
# title => name of the column to use as entry title
# link => name of the column to use as entry link
# date => name of the column to use as entry date
#         May be a Time,String or Numeric column
# desc => name of the column to use as entry content ("description")
#
#
# Examples
#
# http://scraperwikiviews.com/run/rss_2/?scraper=alertbox
# http://scraperwikiviews.com/run/rss_2/?scraper=communication_log&link=uri&date=date_submitted_c&title=behalf&table=contact&order=date_submitted_c  

ScraperWiki.httpresponseheader('Content-Type', 'application/rss_xml')

query_string = ENV["QUERY_STRING"]

raise "Missing QUERY_STRING" if query_string.nil? 

params = query_string.split("&").inject({}) do |memo, p|
  key, val = p.split("=")
  memo[key]= val
  memo
end

raise "Missing 'scraper' param" unless params["scraper"]

scraper = params["scraper"]
title = params["title"] || "title"
link = params["link"] || "link"
description = params["desc"] || "description"
date = params["date"] || "date"

table = params["table"] || "swdata"
limit = params["limit"] || 20
order = params["order"] || date

raise unless scraper

ScraperWiki.attach(scraper)
data = ScraperWiki.select("* from #{table} order by #{order} desc limit #{limit}")

rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = scraper
  m.channel.link = "https://scraperwiki.com/scrapers/%s"% params["scraper"]
  m.channel.description = "RSS feed from ScraperWiki - %s" % params["scraper"]

  data.each do |entry|
    item = m.items.new_item
    item.title = entry[title] || ""
    item.link = entry[link] || ""
    item.description = entry[description] || ""
    item.date = case entry[date]
        when Numeric then Time.at(entry[date])
        when Time then entry[date]
        when String then Time.parse(entry[date]) 
        else Time.new
      end
  end
end

puts rss