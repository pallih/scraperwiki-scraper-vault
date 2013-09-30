require 'nokogiri'

url = "http://feeds.feedburner.com/KumpulanSitusSunnah?fmt=xml"
atom = ScraperWiki.scrape(url)

doc = Nokogiri::XML(atom)
items = doc.xpath("//item")
puts items