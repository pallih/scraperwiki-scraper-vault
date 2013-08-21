# Blank Ruby

html = ScraperWiki::scrape("http://www.realworld.jp/crowd/ranking/daily")
#p html

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("//div[@id='ranking']/ul/li").each do |v|
puts v[0].content
  cells = v.search("//span")
#  if cells.count == 2
    data = {
      rankname: cells[0].content,
      pt:       cells[1].content,
      yen:      cells[2].content
    }
#    puts data.to_json
    ScraperWiki::save_sqlite(['rankname'], data)
#  end
end
