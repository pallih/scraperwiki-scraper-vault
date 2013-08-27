# encoding: UTF-8

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'UTF-8')
doc.search('ul> li').each do |senadoryelecto|
  x = senadoryelecto.inner_html
  puts x

end
# encoding: UTF-8

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'UTF-8')
doc.search('ul> li').each do |senadoryelecto|
  x = senadoryelecto.inner_html
  puts x

end
# encoding: UTF-8

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html 

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'UTF-8')
doc.search('ul> li').each do |senadoryelecto|
  x = senadoryelecto.inner_html
  puts x

end
