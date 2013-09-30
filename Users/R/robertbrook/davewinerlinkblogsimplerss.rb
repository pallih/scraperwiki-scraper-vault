require 'nokogiri'

url = "http://links.scripting.com/rss.xml"
atom = ScraperWiki.scrape(url)

doc = Nokogiri::XML(atom)
items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("description").text
  link = item.xpath("link").text
  published = item.xpath("pubDate").text
  guid = item.xpath("guid").text

  record = {'title' => title, 'link' => link, 'published' => published, 'guid' => guid}
  ScraperWiki.save(['guid'], record)
end
require 'nokogiri'

url = "http://links.scripting.com/rss.xml"
atom = ScraperWiki.scrape(url)

doc = Nokogiri::XML(atom)
items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("description").text
  link = item.xpath("link").text
  published = item.xpath("pubDate").text
  guid = item.xpath("guid").text

  record = {'title' => title, 'link' => link, 'published' => published, 'guid' => guid}
  ScraperWiki.save(['guid'], record)
end
