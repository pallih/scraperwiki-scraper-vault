require 'nokogiri'
root = "http://www.voyage.gc.ca/"

html = ScraperWiki.scrape("http://www.voyage.gc.ca/countries_pays/menu-eng.asp")
doc = Nokogiri::XML(html)

countries = doc.css("a").select {|e| e["href"] && e["href"][/rapport-eng/]}.map {|e| {e.text.strip => e["href"]} }

puts countries

require 'nokogiri'
root = "http://www.voyage.gc.ca/"

html = ScraperWiki.scrape("http://www.voyage.gc.ca/countries_pays/menu-eng.asp")
doc = Nokogiri::XML(html)

countries = doc.css("a").select {|e| e["href"] && e["href"][/rapport-eng/]}.map {|e| {e.text.strip => e["href"]} }

puts countries

