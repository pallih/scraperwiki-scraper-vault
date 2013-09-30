puts "Now extracting senators numbers..."

html = ScraperWiki.scrape("http://www.senate.gov/general/contact_information/senators_cfm.cfm)
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html)
for v in doc.search("div[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
      'senator' => cells[0].inner_html,
      'phone' => cells[4].inner_html.to_i
  }
  ScraperWiki.save_sqlite(unique_keys=['senator', 'phone'], data=data)
endputs "Now extracting senators numbers..."

html = ScraperWiki.scrape("http://www.senate.gov/general/contact_information/senators_cfm.cfm)
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html)
for v in doc.search("div[@align='left'] tr.tcont")
  cells = v.search('td')
  data = {
      'senator' => cells[0].inner_html,
      'phone' => cells[4].inner_html.to_i
  }
  ScraperWiki.save_sqlite(unique_keys=['senator', 'phone'], data=data)
end