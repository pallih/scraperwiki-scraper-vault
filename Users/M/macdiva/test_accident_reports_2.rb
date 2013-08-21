#for ("/html/body/form/div/table[3]/tbody/tr[2]")[0]
html = ScraperWiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=50070")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
  title = td.at_css('small') && td.at_css('small').inner_text
  value = td.at_css('.formdata') && td.at_css('.formdata').inner_text
  next unless title && value
  puts title, value
  ScraperWiki.save(['title', 'data'], {'title' => title, 'data' => value })
end


