# Dangerous countries advisory

require 'nokogiri'
require 'iconv'

html = ScraperWiki::scrape('http://www.voyage.gc.ca/countries_pays/menu-eng.asp')
a = Nokogiri::XML html
warnings = {}

a.search('span.red').each do |el|
  var = el.previous_sibling.previous_sibling
  name = Iconv.iconv('utf-8','iso-8859-1',var.text)[0].strip
  data = {
      country: name,
      url: "http://www.voyage.gc.ca"+var[:href]
  }
  puts data[:url];
  #ScraperWiki::save_sqlite(['country'],data)   

  countryHTML = ScraperWiki::scrape(data[:url])
  scrape = Nokogiri::XML countryHTML
  scrape.search('br + br + strong + br + br').each do |reason|
      puts reason.previous_sibling.previous_sibling

    if reason.previous_sibling.previous_sibling == '3. SAFETY AND SECURITY'
      puts reason.previous_sibling.previous_sibling
    end
#    warnings[reason.previous_sibling.previous_sibling] = ""
  end
end
puts warnings