require 'nokogiri'

html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

doc = Nokogiri::HTML(html)
for v in doc.search("table[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'years_in_school' => cells[4].inner_html.to_i
  }
  puts data.to_json

  ScraperWiki.save_sqlite(unique_keys=['country'], data=data)
end

require 'nokogiri'

html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

doc = Nokogiri::HTML(html)
for v in doc.search("table[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'years_in_school' => cells[4].inner_html.to_i
  }
  puts data.to_json

  ScraperWiki.save_sqlite(unique_keys=['country'], data=data)
end

