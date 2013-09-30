# Blank Ruby
html = ScraperWiki.scrape("http://www.bloomberg.com/markets/rates-bonds/key-rates/")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
  puts td.inner_html
end

doc.search('td').each do |td|
  ScraperWiki.save(unique_keys=['table_cell',], data={'table_cell' => td.inner_html})
end# Blank Ruby
html = ScraperWiki.scrape("http://www.bloomberg.com/markets/rates-bonds/key-rates/")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
  puts td.inner_html
end

doc.search('td').each do |td|
  ScraperWiki.save(unique_keys=['table_cell',], data={'table_cell' => td.inner_html})
end