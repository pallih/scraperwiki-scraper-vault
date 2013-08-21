require 'nokogiri'

xml = ScraperWiki.scrape("http://feed.dilbert.com/dilbert/daily_strip")
rss_doc = Nokogiri::XML(xml)
html = rss_doc.xpath("//item[1]/description/text()")

matches = html.to_s.match(/img src="([^"]+)/)

ScraperWiki.save_sqlite( unique_keys=[ "id" ], data={ "id" => 1, "url" => matches[1] } )

puts matches[1]