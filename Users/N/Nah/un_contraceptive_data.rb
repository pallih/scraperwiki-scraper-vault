require 'nokogiri'           

html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/contraceptive.htm")           

doc = Nokogiri::HTML(html)
for v in doc.search("table[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'modern_methods' => cells[6].child.inner_html.to_i,
    'year' => cells[2].child.inner_html.to_i,
    'any_method' => cells[5].child.inner_html.to_i
  }
      ScraperWiki.save_sqlite(unique_keys=['country'], data=data)
end