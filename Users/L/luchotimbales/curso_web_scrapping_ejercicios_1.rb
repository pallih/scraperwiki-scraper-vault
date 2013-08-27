# Curso web scraping básico - ejercicio 1

html = ScraperWiki.scrape("http://www.infogob.com.pe/Localidad/nacionalprocesodetalle.aspx?IdUbigeo=000000&IdTab=1&IdProceso=00&IdTipoProceso=01")
puts html

require 'nokogiri'

contador=1
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('table[@id="ctl00_ContentPlaceHolder1_detalleproceso_orgpol1_gvOrgPol"]> tr').each do |row|
  puts row  
  if contador ==1 then
  
  else
    $organizacion=row.css("td")[0].text
    $votos=row.css("td")[3].text
    $porcentaje=row.css("td")[4].text
    
    record={}
    record["organizacion"]= $organizacion
    record["votos"]= $votos
    record["porcentaje"]= $procentaje
    ScraperWiki.save_sqlite(["organizacion"], record)
  end
  puts contador
  contador=contador+1
end


# Curso web scraping básico - ejercicio 1

html = ScraperWiki.scrape("http://www.infogob.com.pe/Localidad/nacionalprocesodetalle.aspx?IdUbigeo=000000&IdTab=1&IdProceso=00&IdTipoProceso=01")
puts html

require 'nokogiri'

contador=1
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('table[@id="ctl00_ContentPlaceHolder1_detalleproceso_orgpol1_gvOrgPol"]> tr').each do |row|
  puts row  
  if contador ==1 then
  
  else
    $organizacion=row.css("td")[0].text
    $votos=row.css("td")[3].text
    $porcentaje=row.css("td")[4].text
    
    record={}
    record["organizacion"]= $organizacion
    record["votos"]= $votos
    record["porcentaje"]= $procentaje
    ScraperWiki.save_sqlite(["organizacion"], record)
  end
  puts contador
  contador=contador+1
end


# Curso web scraping básico - ejercicio 1

html = ScraperWiki.scrape("http://www.infogob.com.pe/Localidad/nacionalprocesodetalle.aspx?IdUbigeo=000000&IdTab=1&IdProceso=00&IdTipoProceso=01")
puts html

require 'nokogiri'

contador=1
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('table[@id="ctl00_ContentPlaceHolder1_detalleproceso_orgpol1_gvOrgPol"]> tr').each do |row|
  puts row  
  if contador ==1 then
  
  else
    $organizacion=row.css("td")[0].text
    $votos=row.css("td")[3].text
    $porcentaje=row.css("td")[4].text
    
    record={}
    record["organizacion"]= $organizacion
    record["votos"]= $votos
    record["porcentaje"]= $procentaje
    ScraperWiki.save_sqlite(["organizacion"], record)
  end
  puts contador
  contador=contador+1
end


