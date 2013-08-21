# -*- coding: utf-8 -*-
require "nokogiri"

html = ScraperWiki.scrape('http://www.city.osaka.lg.jp/eventkanko_top/category/715-5-2-0-0.html')

doc = Nokogiri::HTML(html)
puts doc

ul = doc.search("//div")
puts ul.length


#puts data
#    puts data.to_json
#    ScraperWiki.save_sqlite(unique_keys=['date'], data=data)


