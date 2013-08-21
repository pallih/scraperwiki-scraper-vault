# test Ruby
html =ScraperWiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
puts html
require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("div[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'year' => cells[1].inner_html.to_i,
    'years_in_school' => cells[4].inner_html.to_i,
    'men' => cells[7].inner_html.to_i,
    'women' => cells[10].inner_html.to_i
  }
  puts data.to_json

  ScraperWiki.save_sqlite(unique_keys=['country'], data=data)
end
