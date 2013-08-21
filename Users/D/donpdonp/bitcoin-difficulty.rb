require 'nokogiri'
require 'time'

html = ScraperWiki.scrape("http://nullvoid.org/bitcoin/difficultiez.php")

lines = html.split("<br>")
blocks = lines.select{|l| l[0,5] == "Block"}

blocks.each do |block|
  matches = block.match(/Block\s+(\d+)\s+.*\((.*)\).*Difficulty:\s+(\d+\.\d+)/)
  bhash = {"id" => matches[1],
           "date" => Time.parse(matches[2]),
           "difficulty" => "%0.1f" % matches[3]}
  ScraperWiki.save(["id"], bhash, bhash["date"])
end
