html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html

# parse it at XML

require 'nokogiri'
doc = Nokogiri::XML xml
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    puts data.to_json
    #ScraperWiki::save_sqlite(['country'], data)
  end
end


html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html

# parse it at XML

require 'nokogiri'
doc = Nokogiri::XML xml
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    puts data.to_json
    #ScraperWiki::save_sqlite(['country'], data)
  end
end


