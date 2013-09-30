require 'nokogiri'
require 'date'

html = ScraperWiki.scrape("http://www.macapartments.com/illinois/chicago/")
puts html[0..100]
doc = Nokogiri::HTML(html)

id = 0
thisday = Date.today.to_s

doc.css("table tr.text").each do |row|
  cells = row.css("td")
  id = id.next
  data = { :date    => thisday,
           :id      => id,
           :address => cells[1].css("a").inner_html.to_s.strip,
           :unit    => cells[2].inner_html.to_s.strip,
           :beds    => cells[3].inner_html.to_s.strip,
           :baths   => cells[4].inner_html.to_s.strip.to_f,
           :price   => cells[5].inner_html.to_s.strip.delete("$,").to_f }
  ScraperWiki.save_sqlite([:date, :id], data, table_name="listings")
end

require 'nokogiri'
require 'date'

html = ScraperWiki.scrape("http://www.macapartments.com/illinois/chicago/")
puts html[0..100]
doc = Nokogiri::HTML(html)

id = 0
thisday = Date.today.to_s

doc.css("table tr.text").each do |row|
  cells = row.css("td")
  id = id.next
  data = { :date    => thisday,
           :id      => id,
           :address => cells[1].css("a").inner_html.to_s.strip,
           :unit    => cells[2].inner_html.to_s.strip,
           :beds    => cells[3].inner_html.to_s.strip,
           :baths   => cells[4].inner_html.to_s.strip.to_f,
           :price   => cells[5].inner_html.to_s.strip.delete("$,").to_f }
  ScraperWiki.save_sqlite([:date, :id], data, table_name="listings")
end

