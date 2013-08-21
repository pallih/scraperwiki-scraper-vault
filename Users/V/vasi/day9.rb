require 'nokogiri'
html = ScraperWiki::scrape("http://blip.tv/day9tv/rss")
doc = Nokogiri::XML(html)
doc.xpath('//media:content[@height!=720 or @type!="video/x-m4v"]').remove
doc.xpath('//enclosure').remove
ScraperWiki::save_var("rss", doc.to_xml)

