require 'nokogiri'

html = ScraperWiki::scrape("http://www.ns.nl/storingen/index.rss")
doc = Nokogiri::HTML(html)

items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("title").text
  date = item.xpath("pubdate").text
  description = item.xpath("description").text

  ScraperWiki::save_sqlite(unique_keys=["date"], data={"date"=>date, "title"=>title, "description"=>description})
end
require 'nokogiri'

html = ScraperWiki::scrape("http://www.ns.nl/storingen/index.rss")
doc = Nokogiri::HTML(html)

items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("title").text
  date = item.xpath("pubdate").text
  description = item.xpath("description").text

  ScraperWiki::save_sqlite(unique_keys=["date"], data={"date"=>date, "title"=>title, "description"=>description})
end
