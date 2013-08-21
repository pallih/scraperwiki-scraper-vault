require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'yaml'
require 'date'
require 'sanitize'

username = 'umts1900'

url = "http://www.twitter.com/#{username}"

doc = Nokogiri.HTML(open(url))

tweets = doc.search('.stream-item')

# If the table doesn't exist, create it (trust me on this one!)
ScraperWiki.select("* from swdata") rescue ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`time` text, `permalink` text, `tweet` text,`tweettext` text, `lat` real, `lng` real)')
ScraperWiki.select("* from metadata") rescue ScraperWiki.sqliteexecute('CREATE TABLE `metadata` (`username` text, `name` text)')

meta = {}
meta[:username] = username
meta[:name] = doc.search('h1.fullname')[0].inner_text
ScraperWiki::save_sqlite([:username], meta, table_name="metadata", verbose=2)

tweets.each do |tweet|
  
  details = {}
  details[:time] = DateTime.strptime(tweet.search('._timestamp')[0]["data-time"], '%s')
  details[:permalink] = "http://www.twitter.com" + tweet.search('.tweet-timestamp')[0][:href]
  
  source = tweet.search('.username b')[0].inner_text.strip
  tweet_content = Sanitize.clean(tweet.search('.js-tweet-text')[0].inner_html.strip, :elements => ['a'], :attributes => {'a' => ['href']}).gsub("href=\"/", "href=\"http://www.twitter.com/")

  if source.downcase != username.downcase
    # This is a retweet
    details[:tweet] = "RT <a href=\"http://twitter.com/#{source}\">@#{source}</a> " + tweet_content
  else
    details[:tweet] = tweet_content
  end

  if tweet.search('.sm-geo').length > 0
    latlng = tweet.search('.tweet')[0]["data-expanded-footer"].scan(/maps.google.com\/maps\?q=(-?[0-9]+.[0-9]+)%2C(-?[0-9]+.[0-9]+)/)[0]
    details[:lat] = latlng[0]
    details[:lng] = latlng[1]
  end

  details[:tweettext] = Nokogiri::HTML(details[:tweet]).inner_text
 
  if (details[:tweettext].include? 'UT')
    ScraperWiki.save([:permalink], details)
  end

end