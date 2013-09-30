require 'nokogiri'

dataset = Array.new

html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")           

doc = Nokogiri::HTML(html)
for v in doc.search("div[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    :country => cells[0].inner_html,
    :years_in_school => cells[4].inner_html.to_i
  }
 
  dataset.push(data)
end

ScraperWiki.save_sqlite(unique_keys=['country'], data=dataset)           

puts dataset.sort { |x, y| x[:years_in_school] <=> y[:years_in_school] }require 'nokogiri'

dataset = Array.new

html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")           

doc = Nokogiri::HTML(html)
for v in doc.search("div[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    :country => cells[0].inner_html,
    :years_in_school => cells[4].inner_html.to_i
  }
 
  dataset.push(data)
end

ScraperWiki.save_sqlite(unique_keys=['country'], data=dataset)           

puts dataset.sort { |x, y| x[:years_in_school] <=> y[:years_in_school] }