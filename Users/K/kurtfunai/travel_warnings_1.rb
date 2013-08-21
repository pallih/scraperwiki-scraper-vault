# Dangerous countries advisory

require 'nokogiri'
require 'iconv'

html = ScraperWiki::scrape('http://www.voyage.gc.ca/countries_pays/menu-eng.asp')
a = Nokogiri::XML html
ScraperWiki::sqliteexecute('DELETE FROM swdata where country <> ""')

a.search('span.red').each do |el|
  var = el.previous_sibling.previous_sibling
  name = Iconv.iconv('utf-8','iso-8859-1',var.text)[0].strip
  data = {
      country: name,
      url: "http://www.voyage.gc.ca"+var[:href]
  }
  #puts data
  ScraperWiki::save_sqlite(['country'],data)     
end