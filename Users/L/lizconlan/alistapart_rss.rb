require 'nokogiri'

url = "http://alistapart.com/site/abridged-feed"
atom = ScraperWiki.scrape(url)

doc = Nokogiri::XML(atom)
items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("title").text
  link = item.xpath("link").text
  published = item.xpath("dc:date").text
  guid = item.xpath("guid").text
  subject = item.xpath("dc:subject").text

  record = {'title' => title, 'link' => link, 'published' => published, 'guid' => guid, 'subject' => subject}
  ScraperWiki.save(['guid'], record)
end
require 'nokogiri'

url = "http://alistapart.com/site/abridged-feed"
atom = ScraperWiki.scrape(url)

doc = Nokogiri::XML(atom)
items = doc.xpath("//item")

items.each do |item|
  title = item.xpath("title").text
  link = item.xpath("link").text
  published = item.xpath("dc:date").text
  guid = item.xpath("guid").text
  subject = item.xpath("dc:subject").text

  record = {'title' => title, 'link' => link, 'published' => published, 'guid' => guid, 'subject' => subject}
  ScraperWiki.save(['guid'], record)
end
