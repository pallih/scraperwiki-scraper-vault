# Blank Ruby
sourcescraper = 'fred_wilsons_twitter_followers_in_liverpool'

puts "<h1>List of Fred Wilson's Twitter Followers in Liverpool</h1>"
puts "<p>Just a simple view of <a href='http://scraperwiki.com/scrapers/fred_wilsons_twitter_followers_in_liverpool/'>this scraper</a> to make it easier to click through to the followers twitter accounts.</p>"

ScraperWiki.attach(sourcescraper)

puts "<ul>"
ScraperWiki.select( "screen_name from fred_wilsons_twitter_followers_in_liverpool.swdata" ).each do |follower|
  screen_name = follower['screen_name']
  puts "<li><a href='http://twitter.com/#{screen_name}'>#{screen_name}</a></li>"
end
puts "</ul>"


