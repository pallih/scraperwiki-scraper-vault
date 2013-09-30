# Spanish Congress' Publications simple list view
require 'json'

sourcescraper = 'spanish_congress_publications'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("* from swdata limit 10")

puts JSON.generate data

# Spanish Congress' Publications simple list view
require 'json'

sourcescraper = 'spanish_congress_publications'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("* from swdata limit 10")

puts JSON.generate data

