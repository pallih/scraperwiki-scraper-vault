require 'nokogiri'           

baseurl = "http://www.qlife.jp/meds/rx"
doc_type = ".html"
id = "100"

puts [baseurl, id, doc_type].join("")

html = ScraperWiki.scrape([baseurl, id, doc_type].join(""))


doc = Nokogiri::HTML(html)
puts doc

puts doc.css("#leftmenu_dt").to_json
