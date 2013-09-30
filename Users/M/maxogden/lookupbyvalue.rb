# find row by attribute value
# to query: http://scraperwikiviews.com/run/lookupbyvalue/?name:Youth%20Fund

require 'cgi'
ScraperWiki.httpresponseheader("Content-Type", "application/json")
sourcescraper = 'boston-contacts'
keys = ScraperWiki.getKeys(sourcescraper)
column, value = CGI.unescape(ENV['URLQUERY']).split(':')
column = keys[keys.index(column)]
data = ScraperWiki.getData(sourcescraper).map
row = data.find{|d| d[column] == value}
puts row.to_json
# find row by attribute value
# to query: http://scraperwikiviews.com/run/lookupbyvalue/?name:Youth%20Fund

require 'cgi'
ScraperWiki.httpresponseheader("Content-Type", "application/json")
sourcescraper = 'boston-contacts'
keys = ScraperWiki.getKeys(sourcescraper)
column, value = CGI.unescape(ENV['URLQUERY']).split(':')
column = keys[keys.index(column)]
data = ScraperWiki.getData(sourcescraper).map
row = data.find{|d| d[column] == value}
puts row.to_json
