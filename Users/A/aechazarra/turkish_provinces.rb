####ATENCIÓN:::::: Luis está toqueteando#########################################
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

url= "http://www.belgenet.net/ayrinti.php?yil_id=15"  # una URL cualquiera
html= ScraperWiki.scrape(url) # la scrapeamos
puts html # puts sirve para mostrar la información en la hoja de resultados

# 1. Buscar tabla dentro del html

i=0
require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
doc = Nokogiri::HTML(html, nil, 'iso-8859-9') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select" 

  if i==0 or i==1 then
    i=i+1
  else
    puts "Row: "+ row
    puts "Value: "+ row.attr('value') # mostramos los "values"
    puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
    ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
    puts "Name Prov: "+ row.inner_html.split('-').last # mostramos dentro del html solo la ultima parte

    province={} # declaramos un array para guardar los valores
    province["Value"]=row.attr('value') # guardamos por partes
    province["Code Province"]=row.inner_html.split('-').first
    province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
    ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
    puts "saved on database"
    i=i+1
  end
end

####ATENCIÓN:::::: Luis está toqueteando#########################################
# Script Ruby para enseñar como sacar datos de la página http://www.belgenet.net

url= "http://www.belgenet.net/ayrinti.php?yil_id=15"  # una URL cualquiera
html= ScraperWiki.scrape(url) # la scrapeamos
puts html # puts sirve para mostrar la información en la hoja de resultados

# 1. Buscar tabla dentro del html

i=0
require 'nokogiri' # nokogiri es el programa que hace búsquedas dentro de la página
doc = Nokogiri::HTML(html, nil, 'iso-8859-9') # "doc" es el nombre del documento e "iso-8859-9" el formato que se puede ver al principio de la página html
doc.search('select[@class="select"] > option').each do |row| # aquí nos quedamos con las "option" de la tabla "select" del tipo "class=select" 

  if i==0 or i==1 then
    i=i+1
  else
    puts "Row: "+ row
    puts "Value: "+ row.attr('value') # mostramos los "values"
    puts "Code Prov: " +row.inner_html.split('-').first # mostramos dentro del html solo la primera parte
    ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
    puts "Name Prov: "+ row.inner_html.split('-').last # mostramos dentro del html solo la ultima parte

    province={} # declaramos un array para guardar los valores
    province["Value"]=row.attr('value') # guardamos por partes
    province["Code Province"]=row.inner_html.split('-').first
    province["Name Province"]=row.inner_html.split('-').last.encode('UTF-8')
    ScraperWiki.save_sqlite(["Value"], province) #con esta linea guardamos el array poniendo como ID unico "Value"
    puts "saved on database"
    i=i+1
  end
end

