url= "http://elpais.com/tag/fundacion_juan_march/a/11"
html= ScraperWiki.scrape(url)

puts html

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
end


