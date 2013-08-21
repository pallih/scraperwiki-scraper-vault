require 'nokogiri'

url = "http://en.wikipedia.org/wiki/Telephone_numbers_in_the_Netherlands"
doc = Nokogiri::HTML(ScraperWiki.scrape(url))

table = doc.xpath(".//table[@class='multicol']")

puts table.text

columns = table.xpath("./tr/td/p").text

puts columns

rows  = columns.split("\n")

rows.map! do |row|
  md = row.match /^(\d+) (.+)$/
  areacode, name = md[1..2]
end

unique_keys = ['name']

rows.each do |areacode, name|
  # split multinames, discarding all but the first
  name = name.split(",").first
  # strip leading zero from areacode
  areacode.gsub!(/^0/, "")

  result = {'name' => name, 'ac' => areacode}
  #ScraperWiki.save_sqlite(unique_keys, result)
end


