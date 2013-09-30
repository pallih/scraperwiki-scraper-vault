# GNOME Projects
require 'json'

sourcescraper = 'projects_from_doap_file'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("* from swdata")

puts JSON.generate data# GNOME Projects
require 'json'

sourcescraper = 'projects_from_doap_file'
ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select("* from swdata")

puts JSON.generate data