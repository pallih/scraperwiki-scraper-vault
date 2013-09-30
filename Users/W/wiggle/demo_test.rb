# Blank Ruby
p "Hello, coding in the cloud!"
html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html
require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr.tcont").each do |v|
  cells = v.search 'td'
  data = {
    country: cells[0].inner_html,
    years_in_school: cells[4].inner_html.to_i
  }
    ScraperWiki::save_sqlite(['country'], data)

end



# Blank Ruby
p "Hello, coding in the cloud!"
html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html
require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr.tcont").each do |v|
  cells = v.search 'td'
  data = {
    country: cells[0].inner_html,
    years_in_school: cells[4].inner_html.to_i
  }
    ScraperWiki::save_sqlite(['country'], data)

end



