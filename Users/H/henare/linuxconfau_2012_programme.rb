require 'json'
require 'open-uri'

schedule = JSON.parse(open('http://lca2012.linux.org.au/programme/schedule/json').read)

schedule.each do |s|
  ScraperWiki.save_sqlite(["Id"], s)
end
