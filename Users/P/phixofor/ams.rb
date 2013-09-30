# Blank Ruby


require 'rss/1.0'
require 'rss/2.0'
require 'open-uri'

source = "http://www.arbetsformedlingen.se/sitevision/proxy/For-arbetssokande/Lediga-jobb.html/svid12_237ec53d11d47b612d78000171/-123388378/Rss/RssFeed.aspx" # url or local file
content = "" # raw content of rss feed will be loaded here
open(source) do |s| content = s.read end
rss = RSS::Parser.parse(content, false)

numEntries = rss.items.size

i = 1

while i < numEntries  do
  desc = rss.items[i].description
  desc.gsub("<br />", "")

   ScraperWiki.save_sqlite(unique_keys=["description"], data={"description"=>desc})
  i += 1
end

# Blank Ruby


require 'rss/1.0'
require 'rss/2.0'
require 'open-uri'

source = "http://www.arbetsformedlingen.se/sitevision/proxy/For-arbetssokande/Lediga-jobb.html/svid12_237ec53d11d47b612d78000171/-123388378/Rss/RssFeed.aspx" # url or local file
content = "" # raw content of rss feed will be loaded here
open(source) do |s| content = s.read end
rss = RSS::Parser.parse(content, false)

numEntries = rss.items.size

i = 1

while i < numEntries  do
  desc = rss.items[i].description
  desc.gsub("<br />", "")

   ScraperWiki.save_sqlite(unique_keys=["description"], data={"description"=>desc})
  i += 1
end

