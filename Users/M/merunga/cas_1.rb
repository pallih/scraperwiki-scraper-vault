# Blank Ruby

#require 'nokogiri'           
#html = ScraperWiki::scrape("http://empleos.trabajo.gob.pe:8080/empleoperu/Vacante.do?method=listado_vacantes")
#doc = Nokogiri::HTML(html)

#puts doc.xpath("/html/body/table/tbody/tr/td[2]/table/tbody/tr[8]/td/table/tbody/tr[2]/td").size
#puts html

require 'nokogiri'  
http = HTTPClient.new
src = http.get "http://empleos.trabajo.gob.pe:8080/empleoperu/Vacante.do?method=listado_vacantes"
puts src.content
