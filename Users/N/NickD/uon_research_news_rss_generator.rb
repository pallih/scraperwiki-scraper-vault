require 'rss/2.0'

ScraperWiki.httpresponseheader('Content-Type', 'application/rss+xml')
ScraperWiki.attach('uon_research_news')
data = ScraperWiki.select("* from swdata limit 5")

author = "University of Northampton"

rss = RSS::Rss.new("2.0")
channel = RSS::Rss::Channel.new

channel.title = "UoN Research News"
channel.description = "University of Northampton research news"
channel.link = "http://www.northampton.ac.uk/news/20137/research"
channel.language = "en-gb"

data.each do |entry|
  item = RSS::Rss::Channel::Item.new
  item.title = entry['title'] || ""
  item.link = entry['url'] || ""
  item.description = entry['description'] || ""
  #item.date = entry['date']
  item.guid = RSS::Rss::Channel::Item::Guid.new
  item.guid.content = entry['url']
  item.guid.isPermaLink = true
  #item.pubDate = entry['date']
  item.pubDate="Wed, 12 Sep 2012 15:25:04 GMT"
  item.date="Wed, 12 Sep 2012 15:25:04 GMT"
  channel.items << item
end

rss.channel = channel
puts rss

