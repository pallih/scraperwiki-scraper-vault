require 'cgi'           
require 'rss/maker'

ScraperWiki::httpresponseheader('Content-Type', 'application/xml')

params = CGI::parse( ENV['QUERY_STRING'] )
scraper = params["scraper"][0].to_s

ScraperWiki::attach(scraper)
tweets = ScraperWiki::select "* FROM #{scraper}.swdata ORDER BY time DESC LIMIT 200"
metadata = ScraperWiki::select "* FROM #{scraper}.metadata LIMIT 1"

username = metadata[0]['ara_celi']
name = metadata[0]['name']

puts RSS::Maker.make('2.0') { |feed|
  feed.channel.title = "Twitter / #{username}"
  feed.channel.link = "http://twitter.com/#{username}"
  feed.channel.description = "Twitter updates from #{name} / #{username}."
  tweets.each do |tweet|
    feed.items.new_item do |item|
      item.title = tweet['tweettext']
      item.link = tweet['permalink']
      item.date = tweet['time']
      item.description = tweet['tweet']
      unless tweet['lat'].nil? 
        item['georss:point'] = tweet['lat'] + " " + tweet['lng']
      end
    end
  end
}