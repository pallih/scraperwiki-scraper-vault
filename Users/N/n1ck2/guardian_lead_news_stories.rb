# Blank Ruby
puts "Hello world"

require 'rss/1.0'
require 'rss/2.0'
require 'open-uri'

source = "http://feeds.guardian.co.uk/theguardian/rss" # url or local file
content = "" # raw content of rss feed will be loaded here
open(source) do |s| content = s.read end
rss = RSS::Parser.parse(content, false)

numEntries = rss.items.size

i = 1

while i < numEntries  do
  headline = rss.items[i].title
  hyperlink = rss.items[i].link
  ScraperWiki.save_sqlite(unique_keys=["Link", "Headline"], data={"Link"=>hyperlink, "Headline"=>headline})
  i += 1
end

# Blank Ruby
puts "Hello world"

require 'rss/1.0'
require 'rss/2.0'
require 'open-uri'

source = "http://feeds.guardian.co.uk/theguardian/rss" # url or local file
content = "" # raw content of rss feed will be loaded here
open(source) do |s| content = s.read end
rss = RSS::Parser.parse(content, false)

numEntries = rss.items.size

i = 1

while i < numEntries  do
  headline = rss.items[i].title
  hyperlink = rss.items[i].link
  ScraperWiki.save_sqlite(unique_keys=["Link", "Headline"], data={"Link"=>hyperlink, "Headline"=>headline})
  i += 1
end

