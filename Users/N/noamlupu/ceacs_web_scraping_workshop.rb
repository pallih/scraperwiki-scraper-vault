html = ScraperWiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
puts html
puts "*****************Sacamos todas las tablas del html**********************************"


puts "*****************Sacamos la primera columna de la tabla del html que nos interesa**********************************"
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('table[@align="left"]> tr[@class="tcont"]').each do |row|
  $pais= row.css('td')[0].text   
  $fecha= row.css('td')[1].text   
  $dato= row.css('td')[4].text
  puts $pais
  puts $fecha
  puts $dato
  record = {}        
  record['Pais']= $pais
  record['Fecha'] = $fecha
  record['Dato'] = $dato
  ScraperWiki.save_sqlite(["Pais"], record)
end

html = ScraperWiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
puts html
puts "*****************Sacamos todas las tablas del html**********************************"


puts "*****************Sacamos la primera columna de la tabla del html que nos interesa**********************************"
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('table[@align="left"]> tr[@class="tcont"]').each do |row|
  $pais= row.css('td')[0].text   
  $fecha= row.css('td')[1].text   
  $dato= row.css('td')[4].text
  puts $pais
  puts $fecha
  puts $dato
  record = {}        
  record['Pais']= $pais
  record['Fecha'] = $fecha
  record['Dato'] = $dato
  ScraperWiki.save_sqlite(["Pais"], record)
end

