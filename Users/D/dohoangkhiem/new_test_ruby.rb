require 'nokogiri' 
html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
doc = Nokogiri::HTML html 
doc.search("div[@align='left'] tr.tcont").each do |v| 
cells = v.search 'td' 
data = { country: cells[0].inner_html, men: cells[7].inner_html.to_i } 
#puts data.to_json 
print "hello"
ScraperWiki::save_sqlite(['country'], data, "another table 1") 
end 

require 'nokogiri' 
html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm") 
doc = Nokogiri::HTML html 
doc.search("div[@align='left'] tr.tcont").each do |v| 
cells = v.search 'td' 
data = { country: cells[0].inner_html, men: cells[7].inner_html.to_i } 
#puts data.to_json 
print "hello"
ScraperWiki::save_sqlite(['country'], data, "another table 1") 
end 

