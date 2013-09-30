# Blank Ruby
sourcescraper = 'dailydilbert'

ScraperWiki::attach(sourcescraper)

data = ScraperWiki.select("url FROM swdata");

puts "window.location = '"+data[0]["url"]+"'"# Blank Ruby
sourcescraper = 'dailydilbert'

ScraperWiki::attach(sourcescraper)

data = ScraperWiki.select("url FROM swdata");

puts "window.location = '"+data[0]["url"]+"'"