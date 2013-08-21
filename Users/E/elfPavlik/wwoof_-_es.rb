# get page
html = ScraperWiki.scrape("http://ruralvolunteers.org/WHOSTS/publico/whosts_list.php?pagesize=500&language=English")

# parse
require 'nokogiri'
doc = Nokogiri::HTML(html)

rows = doc.css('table tr')

# separate header
header = rows.shift

# get names for columns
column_names = []
header.css('td')[1..-1].each do |cell|
  column_names << cell.text.strip
end

# define columns
ScraperWiki.save_metadata('data_columns', column_names)

# save records
rows.each do |row|
  record = {}
  row.css('td')[1..-1].each_with_index do |cell, index|
    record[column_names[index]] = cell.text.strip
  end
  ScraperWiki.save(['ID'], record)
end
