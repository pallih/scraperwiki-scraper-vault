# Curso web scraping básico - ejercicio 2

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc.search('ul> li> a').each do |row|
  
  #puts row
  $name=row.text
  puts $name

  $url=row.attr("href")
  $url=$url.gsub("javascript:abrir_ventsenarc( '","")
  $url=$url.gsub("')","")
  $url="http://www.senado.es"+$url
  puts $url

  record={}
  record["nombre"]= $name
  record["url"]= $url
  ScraperWiki.save_sqlite(["nombre"], record)

end

# Curso web scraping básico - ejercicio 2

html = ScraperWiki.scrape("http://www.senado.es/legis9/senadores/alfabet.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'iso-8859-1')
doc.search('ul> li> a').each do |row|
  
  #puts row
  $name=row.text
  puts $name

  $url=row.attr("href")
  $url=$url.gsub("javascript:abrir_ventsenarc( '","")
  $url=$url.gsub("')","")
  $url="http://www.senado.es"+$url
  puts $url

  record={}
  record["nombre"]= $name
  record["url"]= $url
  ScraperWiki.save_sqlite(["nombre"], record)

end

