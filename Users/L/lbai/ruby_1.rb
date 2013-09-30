#Some ruby app

html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
p html

require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search("div[@align='left'] tr.tcont").each do |v| 
  cells = v.search 'td'
  data = {
      country: cells[0].inner_html,
      men: cells[5].inner_html,
      women: cells[6].inner_html.to_i,
      years: cells[4].inner_html.to_i,
  }
  #puts data.to_json 
  ScraperWiki::save_sqlite(['country','men','women','years'], data)
end
#Some ruby app

html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
p html

require 'nokogiri'

doc = Nokogiri::HTML(html)

doc.search("div[@align='left'] tr.tcont").each do |v| 
  cells = v.search 'td'
  data = {
      country: cells[0].inner_html,
      men: cells[5].inner_html,
      women: cells[6].inner_html.to_i,
      years: cells[4].inner_html.to_i,
  }
  #puts data.to_json 
  ScraperWiki::save_sqlite(['country','men','women','years'], data)
end
