# Blank Ruby
html = ScraperWiki.scrape("http://soccernet.espn.go.com/tables/_/league/wal.1/season/2010/welsh-premier-league?cc=5739")

require 'nokogiri'
doc = Nokogiri::HTML(html)

clubs = doc.css("div.mod-table tbody tr")
puts clubs.length
clubs.each do |club|
  cells = club.search('td')
  data = {
    'pos' => cells[0].content.to_i,
    'name' => cells[2].content
  }
  # puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['pos'], data=data)           
end