html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

require 'nokogiri'

doc = Nokogiri::HTML(html)
for v in doc.search("table[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'years_in_school' => cells[1].inner_html
  }
  ScraperWiki.save(unique_keys=['country'], data=data)
end
html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

require 'nokogiri'

doc = Nokogiri::HTML(html)
for v in doc.search("table[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
    'country' => cells[0].inner_html,
    'years_in_school' => cells[1].inner_html
  }
  ScraperWiki.save(unique_keys=['country'], data=data)
end
